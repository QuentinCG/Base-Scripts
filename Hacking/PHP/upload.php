<?php
/*
 * \brief Tool to upload any file in server (not secured)
 *
 * \author Quentin Comte-Gaz <quentin@comte-gaz.com>
 * \date 11 August 2016
 * \license MIT License (contact me if too restrictive)
 * \copyright Copyright (c) 2016 Quentin Comte-Gaz
 * \version 1.0
 */
?>
<!DOCTYPE html>
<html>
  <body>
    <form action="upload.php" method="post" enctype="multipart/form-data">
      Select any file to upload:</br>
      <input type="file" name="file_to_upload" id="file_to_upload"><br/>
      <input type="text" name="path" value="" id="path"><br/>
      <input type="submit" value="Upload" name="submit">
    </form>
<?php

if (($_FILES['file_to_upload']['error'] != UPLOAD_ERR_NO_FILE) && isset($_POST['path'])) {
  $target_dir = $_POST['path'];
  $target_file = $target_dir.basename($_FILES["file_to_upload"]["name"]);

  if (move_uploaded_file($_FILES["file_to_upload"]["tmp_name"], $target_file)) {
    echo "The file ".basename($_FILES["file_to_upload"]["name"])." has been uploaded to '".$target_file."'.<br/>";
  } else {
    echo "Can't upload '".$_FILES["file_to_upload"]["name"]."' file to '".$target_file."'.<br/>";
    print_r($_FILES);
  }
}

?>
  </body>
</html>
