import coll2merge


def test_load_restore():
    """Test that loading a file and restoring it returns the same thing."""
    file = './files/simple.coll2'
    # Load using coll2merge
    c = coll2merge.Collection()
    with open(file, 'r') as f:
        c.add_file(f)
    # Export using coll2merge
    coll_str = c.get_coll2()
    # Load file directly
    with open(file, 'r') as f:
        coll_str_expected = f.read()
    # Compare
    assert coll_str == coll_str_expected


def test_load_twice():
    """Test that loading a file twice doubles all the entries."""
    file = './files/simple.coll2'
    # Load using coll2merge
    c = coll2merge.Collection()
    with open(file, 'r') as f:
        c.add_file(f)
    with open(file, 'r') as f:
        c.add_file(f)
    # Export using coll2merge
    coll_str = c.get_coll2()
    file_expected = './files/doubled.coll2'
    # Load file directly
    with open(file_expected, 'r') as f:
        coll_str_expected = f.read()
    # Compare
    assert coll_str == coll_str_expected


def test_load_merge():
    """Test merging two files."""
    file1 = './files/half1.coll2'
    file2 = './files/half2.coll2'
    # Load using coll2merge
    c = coll2merge.Collection()
    with open(file1, 'r') as f:
        c.add_file(f)
    with open(file2, 'r') as f:
        c.add_file(f)
    # Export using coll2merge
    coll_str = c.get_coll2()
    file_expected = './files/whole.coll2'
    # Load file directly
    with open(file_expected, 'r') as f:
        coll_str_expected = f.read()
    # Compare
    assert coll_str == coll_str_expected
