<?php
  class Database {
      private $conn;
      private $servername = "";
      private $username = "";
      private $password = "";
      private $dbname = "";

      public function __construct() {
          $this->conn = new mysqli($this->servername, $this->username, $this->password, $this->dbname);

          if ($this->conn->connect_error) {
              die("Connection failed: " . $this->conn->connect_error);
          }
      }

      public function getConnection() {
          return $this->conn;
      }

      public function closeConnection() {
        $this->conn->close();
      }
  }
?>