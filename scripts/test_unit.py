def test_mac_to_id():
    import tools
    mote_id     = 6
    mote_mac    = "00-17-0d-00-00-3f-fe-87"
    assert mote_id == tools.mac_to_id(mote_mac,1461282879)
