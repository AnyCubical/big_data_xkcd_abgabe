<html>
 <head>
  <title>XKCD Searcher</title>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.1/jquery.min.js"></script>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>

 </head>
 <body>
 <?php
    $dir = 'sqlite:/var/www/html/xkcd.db';
    $dbh = new PDO($dir) or die("cannot open the db");
    $dbQuery = "SELECT * FROM xkcd WHERE safe_title like '%" . $_GET['xkcd'] . "%' order by num;";
 ?>
 <center>
 <h1>XKCD Comic Browser</h1>
 <form action="index.php" method="get">
   <div class="form-group">
     <input name="xkcd" placeholder="XKCD Comic Titel"></input>
     <button type="submit" class="btn btn-outline-dark" data-mdb-ripple-color="dark">Suchen</button>
   </div
 </form>

 <div class="container">
    <div class="row">
      <div class="col-sm">
        <h2>Bild</h2>
      </div>
      <div class="col-sm">
        <h2>Titel</h2>
      </div>
      <div class="col-sm">
        <h2>Link</h2>
      </div>
      <br><hr><br> 
      
 <?php
 foreach ($dbh->query($dbQuery) as $row)
  {
  ?>
    
    <div class="col-sm">
      <img src="<?php echo $row['img']; ?>" style="max-width:300px;width:100%">
    </div>
    <div class="col-sm">
      <h3><?php echo $row['safe_title']; ?></h3>
    </div>
    <div class="col-sm">
      <a href="https://xkcd.com/<?php echo $row['num']; ?>/" target="_blank">https://xkcd.com/<?php echo $row['num']; ?>/</a>
    </div>
    <br><hr><br> 
  <?php
    }
  ?>
  </div>
</div>
 </center>
 </body>
</html>
