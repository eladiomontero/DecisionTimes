<head>
<link rel="StyleSheet" href="style.css" type="text/css">
</head>

<!--Gives information that Part III of experiment is finished
    By presing the button, players are redirected to the questionary
-->

<!-- logo -->
<?php include_once("html_header.php"); ?>
<br><br><br><br><br><br><br><br>

<br><br>
<b>

Het experiment is bijna gedaan.  Alvast bedankt voor je deelname.<br><br>

Vooraleer we het experiment kunnen afsluiten moet je alleen nog de volgende vragen beantwoorden. <br><br>

Nadien zal je te zien krijgen wat je hebt verdiend in dit experiment.<br><br>
 
<?php
$_SESSION['step']="questions1".$_SESSION['language'].".php";
?>

<form name="form1" method="post" action="index.php">
Klik <input type="submit" value="here" class="btn" name="submit"> om verder te gaan.
</form><br />

<!--<script type="text/javascript">
setTimeout('document.form1.submit()',1000);
</script>-->
<?php include_once("html_footer.php"); ?>

