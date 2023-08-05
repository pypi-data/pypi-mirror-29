from hypothesis import given, strategies

import cortexpy.test.driver.command as command


@given(strategies.sampled_from((2, 3)))
def test_prunes_two_tips(tmpdir, tip_length):
    # given
    d = command.Prune(tmpdir)
    d.with_records(
        'CCCGC',
        'AACGC',
    )
    d.prune_tips_less_than(tip_length)
    d.with_kmer_size(3)
    expected_nodes = ['CGC']
    if tip_length < 3:
        expected_nodes.extend(['CCC', 'CCG', 'AAC', 'ACG'])

    # when
    expect = d.run()

    # then
    expect.has_nodes(*expected_nodes)
