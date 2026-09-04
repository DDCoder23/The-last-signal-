import sys, pytest, socket
from pathlib import Path
from unittest.mock import patch, MagicMock
from client_python.client import Client

sys.path.insert(0, str(Path(__file__).parent.parent))

class TestClientInitAndConnect:
    """Unit tests for Client.__init__() and Client.connect() methods."""

    def test_init_default_values(self):
        """Test initialization with default values."""
        client = Client()
        assert client.host == "127.0.0.1"
        assert client.port == 5000
        assert client.session_id is None
        assert client.socket is None
        assert not client.connected

    def test_init_custom_values(self):
        """Test initialization with custom values."""
        client = Client(host="192.168.1.1", port=8080)
        assert client.host == "192.168.1.1"
        assert client.port == 8080
        assert client.session_id is None
        assert client.socket is None
        assert not client.connected

    def test_connect_already_connected(self):
        """If client is already connected, return None."""
        client = Client()
        client.connected = True
        result = client.connect()
        assert result is None
        assert client.socket is None

    @patch('socket.socket')
    def test_connect_success(self, mock_socket):
        """Test successful connection to server."""
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance

        client = Client()
        client.connect()

        assert client.connected is True
        assert client.socket is not None
        mock_socket_instance.connect.assert_called_once_with(("127.0.0.1", 5000))
        mock_socket_instance.settimeout.assert_any_call(1)
        mock_socket_instance.settimeout.assert_any_call(None)

    @patch('time.monotonic')
    @patch('socket.socket')
    def test_connect_timeout(self, mock_socket, mock_monotonic):
        """Test connection timeout and raise system exit."""
        mock_socket.return_value = MagicMock()
        mock_monotonic.side_effect = [0, 91]

        with patch('time.sleep'):
            with pytest.raises(SystemExit):
                client = Client()
                client.connect()

        assert client.connected is False

    @patch('time.sleep')
    @patch('socket.socket')
    def test_connect_connection_refused(self, mock_socket, mock_sleep):
        """If ConnectionRefusedError raised, retry connection."""
        mock_socket_instance = MagicMock()
        mock_socket_instance.connect.side_effect = [ConnectionRefusedError(), None]
        mock_socket.return_value = mock_socket_instance

        client = Client()
        client.connect()

        assert client.connected is True
        assert mock_socket_instance.connect.call_count == 2
        mock_sleep.assert_called_once_with(0.5)

    @patch('time.sleep')
    @patch('socket.socket')
    def test_connect_timeout_exception(self, mock_socket, mock_sleep):
        """If socket.timeout raised, retry connection."""
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        mock_socket_instance.connect.side_effect = [socket.timeout(), None]

        client = Client()
        client.connect()

        assert client.connected is True
        assert mock_socket_instance.connect.call_count == 2
        mock_sleep.assert_called_once_with(0.5)

    @patch('socket.socket')
    def test_connect_runtime_exception(self, mock_socket):
        """Test runtime exception raise."""
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        mock_socket_instance.connect.side_effect = RuntimeError("Unexpected error")

        client = Client()
        with pytest.raises(RuntimeError):
            client.connect()

        assert client.connected is False
