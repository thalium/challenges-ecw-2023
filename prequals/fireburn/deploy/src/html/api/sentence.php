<?php

require_once('../includes/config.inc.php');

$id = filter_input(INPUT_GET, "id", FILTER_VALIDATE_INT);

if (!$id) {
    $range = array_merge(range(1, 41), range(43, 50));
    $id = $range[mt_rand(0, count($range)-1)];
}

if (!($dbh = fbird_connect($host, $username, $password))) {
    $tab["errmsg"] = "DB connection error.";
}
$stmt = "SELECT * FROM SENTENCES WHERE ID = $id;";
$sth = fbird_query($dbh, $stmt);
while ($row = fbird_fetch_object($sth)) {
    $tab['status'] = 'ok';
    $tab['id'] = $row->ID;
    $tab['sentence'] = $row->SENTENCE;
}
if (!$tab["status"]) {
    $tab["status"] = "not found";

}
header('Content-Type: application/json');
echo json_encode($tab);

fbird_free_result($sth);
fbird_close($dbh);

?>