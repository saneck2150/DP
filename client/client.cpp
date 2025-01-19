#include <iostream>
#include <fstream>
#include <filesystem>
#include <cstring>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

namespace fs = std::filesystem;

class TCPClient {
private:
    std::string server_ip;
    int server_port;
    int sock;
    std::ofstream log_file;

public:
    TCPClient(const std::string& ip, int port) : server_ip(ip), server_port(port), sock(-1) {
        fs::create_directory("logs");  // Create logs directory if it doesn't exist
        log_file.open("logs/client.log", std::ios::app);
        if (!log_file) {
            std::cerr << "Error opening log file\n";
        }
    }

    ~TCPClient() {
        if (log_file.is_open()) {
            log_file.close();
        }
    }

    bool connect_to_server() {
        sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock == -1) {
            log("Error creating socket");
            return false;
        }

        sockaddr_in server_address{};
        server_address.sin_family = AF_INET;
        server_address.sin_port = htons(server_port);
        if (inet_pton(AF_INET, server_ip.c_str(), &server_address.sin_addr) <= 0) {
            log("Invalid server address");
            return false;
        }

        if (connect(sock, (struct sockaddr*)&server_address, sizeof(server_address)) < 0) {
            log("Failed to connect to server");
            return false;
        }

        log("Connected to server successfully");
        return true;
    }

    void send_message(const std::string& message) {
        log("Sending message: " + message);

        if (send(sock, message.c_str(), message.size(), 0) < 0) {
            log("Error sending message");
            return;
        }

        char buffer[1024] = {0};
        int bytes_received = recv(sock, buffer, sizeof(buffer), 0);
        if (bytes_received < 0) {
            log("Error receiving response");
        } else {
            std::string response(buffer, bytes_received);
            log("Response from server: " + response);
            std::cout << "Server response: " << response << std::endl;
        }
    }

    void close_connection() {
        if (sock != -1) {
            close(sock);
            log("Connection closed");
        }
    }

    void log(const std::string& message) {
        if (log_file.is_open()) {
            log_file << "[LOG] " << message << std::endl;
        }
        std::cout << message << std::endl;
    }
};

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: ./client <message>\n";
        return 1;
    }

    TCPClient client("127.0.0.1", 8888);
    if (client.connect_to_server()) {
        client.send_message(argv[1]);
        client.close_connection();
    }

    return 0;
}
