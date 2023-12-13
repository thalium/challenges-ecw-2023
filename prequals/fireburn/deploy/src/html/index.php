<!doctype html>
<html lang="en">

<head>
    <title>Chat AI</title>
    <link href="/static/css/style.css" rel="stylesheet">
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">
    <link href="/static/css/bootstrap-icons.css" rel="stylesheet">

</head>

<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <a class="navbar-brand" href="/">Chat AI</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbar" aria-controls="navbar"
            aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbar">
            <ul class="navbar-nav mr-auto">
                <li class="nav-item<?php /*if ($page == 'home') { echo " active"; } */?>"><a class="nav-link"
                        href="?page=home">Home</a></li>
            </ul>
        </div>
    </nav>
    <div class="container py-4">
<?php
if (!isset($_GET['page']) || $_GET['page'] == '') {
    $page = 'home';
  } else {
    $page = $_GET['page'];
  }
    
switch ($page) {
    // case 'search':
    //     include('includes/search.php');
    //     break;
    default:
        include('includes/home.php');
        break;
    }
  
?>
    </div>
    <script src="/static/js/jquery.min.js"></script>
    <script src="/static/js/bootstrap.min.js"></script>
    <script src="/static/js/bootstrap.bundle.min.js"></script>
    <script src="/static/js/script.js"></script>
</body>

</html>