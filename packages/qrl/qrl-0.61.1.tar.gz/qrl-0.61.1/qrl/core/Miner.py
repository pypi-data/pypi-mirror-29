# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
import copy
from typing import Optional

from pyqrllib.pyqrllib import bin2hstr
from pyqryptonight.pyqryptonight import Qryptominer, StringToUInt256, UInt256ToString

from qrl.core import config
from qrl.core.Block import Block
from qrl.core.DifficultyTracker import DifficultyTracker
from qrl.core.State import State
from qrl.core.Transaction import Transaction, TransferTransaction, TokenTransaction, TransferTokenTransaction, \
    MessageTransaction, LatticePublicKey, SlaveTransaction
from qrl.core.Wallet import Wallet
from qrl.core.misc import logger


class Miner(Qryptominer):
    def __init__(self, pre_block_logic, slaves: list, state: State, mining_thread_count, add_unprocessed_txn_fn):
        super().__init__()
        self.pre_block_logic = pre_block_logic  # FIXME: Circular dependency with node.py
        self._mining_block = None
        self._slaves = slaves
        self._mining_xmss = None
        self._reward_address = None
        self.state = state
        self._difficulty_tracker = DifficultyTracker()
        self._add_unprocessed_txn_fn = add_unprocessed_txn_fn
        self._mining_thread_count = mining_thread_count
        self._dummy_xmss = None

    @staticmethod
    def set_unused_ots_key(xmss, addr_state, start=0):
        for i in range(start, 2 ** xmss.height):
            if not addr_state.ots_key_reuse(i):
                xmss.set_ots_index(i)
                return True
        return False

    def valid_mining_permission(self):
        if self._master_address == self._mining_xmss.address:
            return True
        addr_state = self.state.get_address(self._master_address)
        access_type = addr_state.get_slave_permission(self._mining_xmss.pk)
        if access_type == -1:
            logger.warning('Slave is not authorized yet for mining')
            logger.warning('Added Slave Txn')
            slave_tx = Transaction.from_json(self._slaves[2])
            self._add_unprocessed_txn_fn(slave_tx, None)
            return None
        return True

    def get_mining_xmss(self):
        if self._mining_xmss:
            addr_state = self.state.get_address(self._mining_xmss.address)
            if self.set_unused_ots_key(self._mining_xmss, addr_state, self._mining_xmss.ots_index):
                if self.valid_mining_permission():
                    return self._mining_xmss
            else:
                self._mining_xmss = None
            return None

        if not self._mining_xmss:
            self._master_address = self._slaves[0]
            unused_ots_found = False
            for slave_seed in self._slaves[1]:
                xmss = Wallet.get_new_address(signature_tree_height=None, seed=slave_seed).xmss
                addr_state = self.state.get_address(xmss.address)
                if self.set_unused_ots_key(xmss, addr_state):  # Unused ots_key_found
                    self._mining_xmss = xmss
                    unused_ots_found = True
                    break

            if not unused_ots_found:  # Unused ots_key_found
                logger.warning('No OTS-KEY left for mining')
                return None

        if self._master_address == self._mining_xmss.address:
            return self._mining_xmss

        if not self.valid_mining_permission():
            return None

        return self._mining_xmss

    def start_mining(self,
                     tx_pool,
                     parent_block: Block,
                     parent_difficulty):

        mining_xmss = self.get_mining_xmss()
        if not mining_xmss:
            logger.warning('No Mining XMSS Found')
            return

        try:
            self.cancel()
            self._mining_block = self.create_block(last_block=parent_block,
                                                   mining_nonce=0,
                                                   tx_pool=tx_pool,
                                                   signing_xmss=self._mining_xmss,
                                                   master_address=self._master_address)

            parent_metadata = self.state.get_block_metadata(parent_block.headerhash)
            measurement = self.state.get_measurement(self._mining_block.timestamp,
                                                     self._mining_block.prev_headerhash,
                                                     parent_metadata)

            current_difficulty, current_target = self._difficulty_tracker.get(
                measurement=measurement,
                parent_difficulty=parent_difficulty)

            mining_blob = self._mining_block.mining_blob
            nonce_offset = self._mining_block.mining_nonce_offset

            logger.debug('!!! Mine #{} | {} ({}) | {} -> {} | {}'.format(
                self._mining_block.block_number,
                measurement, self._mining_block.timestamp - parent_block.timestamp,
                UInt256ToString(parent_difficulty), UInt256ToString(current_difficulty),
                current_target
            ))
            logger.debug('!!! {}'.format(current_target))
            self.start(input=mining_blob,
                       nonceOffset=nonce_offset,
                       target=current_target,
                       thread_count=self._mining_thread_count)
        except Exception as e:
            logger.warning("Exception in start_mining")
            logger.exception(e)

    def solutionEvent(self, nonce):
        # NOTE: This function usually runs in the context of a C++ thread
        try:
            logger.debug('Solution Found %s', nonce)
            self._mining_block.set_mining_nonce(nonce)
            logger.info('Block #%s nonce: %s', self._mining_block.block_number, StringToUInt256(str(nonce))[-4:])
            logger.info('Hash Rate: %s H/s', self.hashRate())
            cloned_block = copy.deepcopy(self._mining_block)
            self.pre_block_logic(cloned_block)
        except Exception as e:
            logger.warning("Exception in solutionEvent")
            logger.exception(e)

    def create_block(self, last_block, mining_nonce, tx_pool, signing_xmss, master_address) -> Optional[Block]:
        # TODO: Persistence will move to rocksdb
        # FIXME: Difference between this and create block?????????????

        # FIXME: Break encapsulation
        if not self._dummy_xmss:
            self._dummy_xmss = Wallet.get_new_address(signature_tree_height=signing_xmss.height)
        dummy_block = Block.create(block_number=last_block.block_number + 1,
                                   prevblock_headerhash=last_block.headerhash,
                                   transactions=[],
                                   signing_xmss=self._dummy_xmss.xmss,
                                   master_address=master_address,
                                   nonce=0)
        dummy_block.set_mining_nonce(mining_nonce)

        t_pool2 = copy.deepcopy(tx_pool.transaction_pool)
        del tx_pool.transaction_pool[:]
        ######

        # recreate the transaction pool as in the tx_hash_list, ordered by txhash..
        total_txn = len(t_pool2)
        txnum = 0
        addresses_set = set()
        while txnum < total_txn:
            tx = t_pool2[txnum]
            tx.set_effected_address(addresses_set)
            txnum += 1

        addresses_state = dict()
        for address in addresses_set:
            addresses_state[address] = self.state.get_address(address)

        block_size = dummy_block.size
        block_size_limit = self.state.get_block_size_limit(last_block)
        txnum = 0
        while txnum < total_txn:
            tx = t_pool2[txnum]
            # Skip Transactions for later, which doesn't fit into block
            if block_size + tx.size + config.dev.tx_extra_overhead > block_size_limit:
                txnum += 1
                continue

            addr_from_pk_state = addresses_state[tx.txfrom]
            addr_from_pk = Transaction.get_slave(tx)
            if addr_from_pk:
                addr_from_pk_state = addresses_state[addr_from_pk]

            if addr_from_pk_state.ots_key_reuse(tx.ots_key):
                del t_pool2[txnum]
                total_txn -= 1
                continue

            if isinstance(tx, TransferTransaction):
                if addresses_state[tx.txfrom].balance < tx.amount + tx.fee:
                    logger.warning('%s %s exceeds balance, invalid tx', tx, tx.txfrom)
                    logger.warning('type: %s', tx.type)
                    logger.warning('Buffer State Balance: %s  Transfer Amount %s', addresses_state[tx.txfrom].balance,
                                   tx.amount)
                    del t_pool2[txnum]
                    total_txn -= 1
                    continue

            if isinstance(tx, MessageTransaction):
                if addresses_state[tx.txfrom].balance < tx.fee:
                    logger.warning('%s %s exceeds balance, invalid message tx', tx, tx.txfrom)
                    logger.warning('type: %s', tx.type)
                    logger.warning('Buffer State Balance: %s  Free %s', addresses_state[tx.txfrom].balance, tx.fee)
                    total_txn -= 1
                    continue

            if isinstance(tx, TokenTransaction):
                if addresses_state[tx.txfrom].balance < tx.fee:
                    logger.warning('%s %s exceeds balance, invalid tx', tx, tx.txfrom)
                    logger.warning('type: %s', tx.type)
                    logger.warning('Buffer State Balance: %s  Fee %s',
                                   addresses_state[tx.txfrom].balance,
                                   tx.fee)
                    del t_pool2[txnum]
                    total_txn -= 1
                    continue

            if isinstance(tx, TransferTokenTransaction):
                if addresses_state[tx.txfrom].balance < tx.fee:
                    logger.warning('%s %s exceeds balance, invalid tx', tx, tx.txfrom)
                    logger.warning('type: %s', tx.type)
                    logger.warning('Buffer State Balance: %s  Transfer Amount %s',
                                   addresses_state[tx.txfrom].balance,
                                   tx.fee)
                    del t_pool2[txnum]
                    total_txn -= 1
                    continue

                if bin2hstr(tx.token_txhash).encode() not in addresses_state[tx.txfrom].tokens:
                    logger.warning('%s doesnt own any token with token_txnhash %s', tx.txfrom,
                                   bin2hstr(tx.token_txhash).encode())
                    del t_pool2[txnum]
                    total_txn -= 1
                    continue

                if addresses_state[tx.txfrom].tokens[bin2hstr(tx.token_txhash).encode()] < tx.amount:
                    logger.warning('Token Transfer amount exceeds available token')
                    logger.warning('Token Txhash %s', bin2hstr(tx.token_txhash).encode())
                    logger.warning('Available Token Amount %s',
                                   addresses_state[tx.txfrom].tokens[bin2hstr(tx.token_txhash).encode()])
                    logger.warning('Transaction Amount %s', tx.amount)
                    del t_pool2[txnum]
                    total_txn -= 1
                    continue

            if isinstance(tx, LatticePublicKey):
                if addresses_state[tx.txfrom].balance < tx.fee:
                    logger.warning('Lattice TXN %s %s exceeds balance, invalid tx', tx, tx.txfrom)
                    logger.warning('type: %s', tx.type)
                    logger.warning('Buffer State Balance: %s  Transfer Amount %s',
                                   addresses_state[tx.txfrom].balance,
                                   tx.fee)
                    del t_pool2[txnum]
                    total_txn -= 1
                    continue

            if isinstance(tx, SlaveTransaction):
                if addresses_state[tx.txfrom].balance < tx.fee:
                    logger.warning('Slave TXN %s %s exceeds balance, invalid tx', tx, tx.txfrom)
                    logger.warning('type: %s', tx.type)
                    logger.warning('Buffer State Balance: %s  Transfer Amount %s',
                                   addresses_state[tx.txfrom].balance,
                                   tx.fee)
                    del t_pool2[txnum]
                    total_txn -= 1
                    continue

            tx.apply_on_state(addresses_state)

            tx_pool.add_tx_to_pool(tx)
            tx._data.nonce = addresses_state[tx.txfrom].nonce
            txnum += 1
            block_size += tx.size + config.dev.tx_extra_overhead

        coinbase_nonce = self.state.get_address(signing_xmss.address).nonce
        if signing_xmss.address in addresses_state:
            coinbase_nonce = addresses_state[signing_xmss.address].nonce + 1

        block = Block.create(block_number=last_block.block_number + 1,
                             prevblock_headerhash=last_block.headerhash,
                             transactions=t_pool2,
                             signing_xmss=signing_xmss,
                             master_address=master_address,
                             nonce=coinbase_nonce)

        return block
