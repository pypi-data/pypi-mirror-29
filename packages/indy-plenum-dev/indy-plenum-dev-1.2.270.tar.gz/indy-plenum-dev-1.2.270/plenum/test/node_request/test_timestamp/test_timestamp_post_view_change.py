from stp_core.loop.eventually import eventually

from plenum.test.helper import send_reqs_to_nodes_and_verify_all_replies, \
    sendRandomRequests, checkViewNoForNodes
from plenum.test.node_request.test_timestamp.helper import make_clock_faulty, \
    get_timestamp_suspicion_count
from plenum.test.test_node import ensureElectionsDone, getNonPrimaryReplicas
from plenum.test.view_change.helper import ensure_view_change
from plenum.test.helper import sdk_send_random_and_check, sdk_send_random_requests
from plenum.test.delayers import icDelay

Max3PCBatchSize = 4

from plenum.test.batching_3pc.conftest import tconf

# lot of requests will be sent and multiple view changes are done
TestRunningTimeLimitSec = 200


def test_new_primary_has_wrong_clock(tconf, looper, txnPoolNodeSet,
                                     sdk_wallet_client, sdk_pool_handle):
    """
    One of non-primary has a bad clock, it raises suspicions but orders
    requests after getting PREPAREs. Then a view change happens this
    non-primary with the bad clock becomes the new primary but is not able to
    get any of it's PRE-PREPAREs ordered. Eventually another view change
    happens and a new primary is elected the pool is functional again
    :return:
    """
    # The node having the bad clock, this node will be primary after view
    # change
    faulty_node = getNonPrimaryReplicas(txnPoolNodeSet, 0)[0].node
    make_clock_faulty(faulty_node)

    assert not faulty_node.master_replica.isPrimary
    # faulty_node replies too
    sdk_send_random_and_check(looper,
                              txnPoolNodeSet,
                              sdk_pool_handle,
                              sdk_wallet_client,
                              count=Max3PCBatchSize * 3)

    ledger_sizes = {
        node.name: node.domainLedger.size for node in txnPoolNodeSet}
    susp_counts = {node.name: get_timestamp_suspicion_count(
        node) for node in txnPoolNodeSet}
    ensure_view_change(looper, txnPoolNodeSet)
    ensureElectionsDone(looper=looper, nodes=txnPoolNodeSet)

    # After view change, faulty_node is primary
    assert faulty_node.master_replica.isPrimary

    old_view_no = txnPoolNodeSet[0].viewNo

    # Delay parameters
    malicious_batch_count = 5
    malicious_batch_interval = 2
    instance_change_delay = 1.5 * malicious_batch_count * malicious_batch_interval

    # Delay instance change so view change doesn't happen in the middle of this test
    for node in txnPoolNodeSet:
        node.nodeIbStasher.delay(icDelay(instance_change_delay))

    # Requests are sent
    for _ in range(malicious_batch_count):
        sdk_send_random_requests(looper,
                                sdk_pool_handle,
                                sdk_wallet_client,
                                count=2)
        looper.runFor(malicious_batch_interval)

    def chk():
        for node in txnPoolNodeSet:
            assert node.viewNo == old_view_no

        for node in [n for n in txnPoolNodeSet if n != faulty_node]:
            # Each non faulty node raises suspicion
            assert get_timestamp_suspicion_count(node) > susp_counts[node.name]
            # Ledger does not change
            assert node.domainLedger.size == ledger_sizes[node.name]

        assert faulty_node.domainLedger.size == ledger_sizes[faulty_node.name]

    looper.run(eventually(chk, retryWait=1))

    # Clear delays
    for node in txnPoolNodeSet:
        node.nodeIbStasher.reset_delays_and_process_delayeds()

    # Eventually another view change happens
    looper.run(eventually(checkViewNoForNodes, txnPoolNodeSet, old_view_no + 1,
                          retryWait=1, timeout=2 * tconf.PerfCheckFreq))
    ensureElectionsDone(looper=looper, nodes=txnPoolNodeSet)

    # After view change, faulty_node is no more the primary
    assert not faulty_node.master_replica.isPrimary

    # All nodes reply
    sdk_send_random_and_check(looper,
                              txnPoolNodeSet,
                              sdk_pool_handle,
                              sdk_wallet_client,
                              count=Max3PCBatchSize * 2)
