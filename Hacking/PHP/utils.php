<?php

/*!
 * \brief Show content of any readable file in server
 * \param filePath (str) Filename or path to file to get content
 * \note If file does not exist, an error message is displayed
 *
 * \examples
 *   displayFileContent('/home/my_user/.bashrc');
 *   displayFileContent('index.php');
 */
function displayFileContent($filePath)
{
  if (($inF = fopen($filePath, "r"))) {
    $inF = fopen($filePath, "r");
    $j="";

    while (!feof($inF)) {
      $j=$j.fgets($inF, 4096);
    }

    echo $j;
    fclose($inF);
  } else {
    echo "Can't open '".$filePath."' file";
  }
}

/*!
 * \brief Display folder and files recursively
 * \param dir (str) Relative path of folder to scan
 *
 * \examples
 *   displayFoldersFiles('./');
 *   displayFoldersFiles('./../..');
 *   displayFoldersFiles('folder_1/folder_2');
 */
function displayFoldersAndFiles($dir){
  $ffs = scandir($dir);
  echo "<ol>\n";
  foreach($ffs as $ff){
    if($ff != '.' && $ff != '..'){
      echo "  <li>";
      if(is_dir($dir."/".$ff)) {
        echo "[folder] ".$ff."\n";
        displayFoldersAndFiles($dir."/".$ff);
      } else {
        echo "[file] ".$ff;
      }
      echo "</li>\n";
    }
  }
  echo "</ol>\n";
}

?>
<?php

// Use all previously defined functions with GET commands
// Example: utils.php?dir=./&file=index.php

if(isset($_GET['file'])) {
  $file = $_GET['file'];
  echo "Content of '".$file."' file:";
  echo "<xmp>";
  displayFileContent($file);
  echo "</xmp>";
}

if(isset($_GET['dir'])) {
  $dir = $_GET['dir'];
  echo 'Files and folders in '.getcwd().'/'.$dir.':';
  displayFoldersAndFiles($dir);
}

?>