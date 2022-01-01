import make_fingerprint as mf

def test_filtering():
    # given
    trace_file_name = "test/data/filtering_test.txt"
    #must_include_head = ["POSI;", "WIFI;", "MAGN;"]
    must_include_head = ["POSI;", "WIFI;"]

    # when
    filtered_lines = mf.filtering(trace_file_name, must_include_head)

    # then
    assert "ACCE;" not in filtered_lines[:100]
    assert len(filtered_lines) == 4

