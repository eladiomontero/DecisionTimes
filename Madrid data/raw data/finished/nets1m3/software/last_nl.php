<head>
<link rel="StyleSheet" href="style.css" type="text/css">
</head>

<!-- logo -->
<?php include_once("html_header.php"); ?>
<br><br><br><br><br><br><br><br>

<?php
$user=$_SESSION['username'];
$total=file_get_contents('data/'.$user.'totalscore');
$point=file_get_contents('data/pointvalue');
$earned=($total)*$point+2.5;

?>

Het experiment is gedaan.<br><br>

Het gewonnen bedrag is: <b>
<?php echo $earned." &#128;"
?> 
</b> 
<br>
<br>

Dit bedrag bevat ook de 2.5 Euro deelnamebeloning. <br><br>

Schrijf dit bedrag op het deelnameformulier.  <br><br>
 
Gelieve te wachten tot de onderzoeker je roept voor de verdere afhandeling van het experiment. Als je geroepen wordt breng dan het ingevulde deelnameformulier naar de onderzoeker zodat de financiële transactie kan worden vervolledigd.<br><br>

Je zal je gebruikersnaam moeten laten zien zodat er kan worden nagegaan of het ingevulde bedrag overeenstemt met het bedrag dat je hebt opgeschreven. <br><br>

<b>Het instructieblad moet worden teruggeven aan de onderzoekers.</b><br><br>

Gelieve geen details over het experiment door te geven aan andere potentiele deelnemers.  Dit zou de studie niet ten goede komen.  Het zou er zelfs toe kunnen leiden dat we gans de studie moeten stopzetten. <br><br>

Bedankt om deel te nemen aan dit experiment.<br><br>

We hopen dat je het leuk vond en dat je in de toekomst terug zal deelnemen aan experimenten die wij organiseren.

<?php include_once("html_footer.php"); ?>

