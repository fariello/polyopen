import pytest
from unittest.mock import patch, MagicMock
from polyopen import polyopen

@patch('paramiko.SSHClient')
def test_ssh_routing(mock_ssh):
    """
    Assert polyopen intercepts ssh:// streams and spins up the paramount infrastructure
    without triggering local file bindings.
    """
    mock_instance = MagicMock()
    mock_ssh.return_value = mock_instance
    
    # We mock open_sftp to intercept and succeed
    mock_sftp = MagicMock()
    mock_instance.open_sftp.return_value = mock_sftp

    with polyopen("ssh://user:pass@host/file.txt", 'w', backup=False) as writer:
        writer.write("stub")
        
    assert mock_ssh.called
    assert mock_instance.connect.called
    assert mock_instance.open_sftp.called

@patch('requests.get')
def test_http_routing(mock_get):
    """
    Assert polyopen cleanly traps http:// streams and yields to the requests pipeline natively.
    """
    mock_response = MagicMock()
    mock_response.headers = {'Content-Length': '100'}
    
    # Mocking standard UTF-8 stream decoding fallback using a true generator
    def mock_iter():
        yield b"line 1\n"
        yield b"line 2\n"
    mock_response.iter_lines.return_value = mock_iter()
    mock_get.return_value = mock_response
    
    lines = []
    with polyopen("https://example.com/data.txt", 'r') as reader:
        for line in reader:
             lines.append(line)
             
    assert mock_get.called
    assert len(lines) == 2
    assert lines[0] == "line 1\n"
