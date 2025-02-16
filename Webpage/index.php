<!doctype html>
<html lang="en" data-bs-theme="auto">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="">
  <meta name="author" content="Riccardo Galdieri">
  <title>Formula 1 Time Tables</title>
  <link rel="icon" href="favicon.ico" type="image/x-icon">
  <link rel="canonical" href="https://getbootstrap.com/docs/5.3/examples/starter-template/">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@docsearch/css@3">
  <link rel="stylesheet" href="main.css">
  <link rel="stylesheet" href="def-style.css">
  <link href="bootstrap/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
  <div class="col-lg-9 mx-auto p-4 py-md-5">
    <header class="site-logo d-flex align-items-center pb-3 mb-5">
      <img src="images/f1-logo.png" />
    </header>
    <?php
      require 'db.php';
      require "functions.php";
      
      $db = new Database();
    
    ?>
    <main>
      <div id="recaps">
        <div class="row record-holders">
          <!-- RECAP -->
          <?php
           GenerateMedals($db);
          ?>

        </div>
        <div id="news">
          <?php
            PopulateNews($db);
          ?>

        </div>
      </div>
      <!-- Circuits -->
      <div>
        <div class="row">
          <?php
            PopulateTables($db);
          ?>
        </div>
      </div>
      <?php
        $db->closeConnection(); 
      ?>
    </main>

    <footer class="pt-5 my-5 text-body-secondary border-top">
      Made by yours truly <a target="_blank" href="https://www.linkedin.com/in/riccardo-galdieri-ph-d-49656a151/">Riccardo Galdieri</a>
    </footer>
  </div>
  <script src="bootstrap/js/bootstrap.bundle.min.js"></script>
</body>
</html>
