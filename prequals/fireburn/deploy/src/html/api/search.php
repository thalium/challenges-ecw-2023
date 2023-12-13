<?php

header('Content-Type: application/json');
require_once('../includes/config.inc.php');

if (!isset($_GET['id']) || empty($_GET['id'])) {
    $id = rand(51, 100);
    $answers = array(
        "It really depends on your personal preferences and needs.",
        "There are many different approaches you could take to address that.",
        "It's important to consider the specific situation before making a decision.",
        "That's a great question, and there are a lot of potential answers.",
        "There are a lot of resources available to help with that.",
        "It's always a good idea to do some research and gather information.",
        "Finding a balance between different factors is key.",
        "It's important to consider both the short-term and long-term implications.",
        "Experimenting and trying new things can often lead to new insights and ideas.",
        "At the end of the day, it's about finding what works best for you."
    );
    echo '{"status":"ok","id":"'.$id.'","answer":"'.$answers[array_rand($answers)].'"}';
} else {
    $id = $_GET['id'];
    $upperid = trim(strtoupper($id));
    
    $blacklist = array(
        'MON$',
        'SEC$',
        ' ',
        //'\'', needed
        '_ISO', '_UTF', '_ASCII', 'X\'', '0X',
        //"ABS", "ACOS", "ACOSH", "ASIN", "ASINH", "ATAN", "ATAN2", "ATANH", "CEIL", "COS", "COSH", "COT", "EXP", "FLOOR",
        //"LN", "LOG", "LOG10", "MOD", "PI", "POWER", "RAND", "ROUND", "SIGN", "SIN", "SINH", "SQRT", "TAN", "TANH", "TRUNC",
        "ASCII_CHAR", "ASCII_VAL", "BIT_LENGTH", "CHAR_LENGTH", "CHARACTER_LENGTH", "HASH", "LEFT", "LOWER", "LPAD",
        "OCTET_LENGTH", "OVERLAY", "POSITION", "REPLACE", "REVERSE", "RIGHT", "RPAD", "SUBTODOSTRING", "TRIM", "UPPER",
        "DATEADD", "DATEDIFF", "EXTRACT", "CAST", "BIN_AND","BIN_NOT", "BIN_OR", "BIN_SHL", "BIN_SHR", "BIN_XOR",
        "CHAR_TO_UUID", "GEN_UUID", "UUID_TO_CHAR", "GEN_ID", "COALESCE", "DECODE", "IIF", "MAXVALUE", "MINVALUE", "NULLIF",
        "AVG", "COUNT", "LIST", "MAX", "MIN", "SUM", "=", "<>", "!=", "~=", "^=", "<", "<=", ">", ">=", "!<", "~<", "^<",
        "!>", "~>", "^>", "+", "-", "/", "*", "^", "|", "NOT", "AND", //OR is filtered below
        "LIKE", "STARTING", "CONTAINING", "BETWEEN", "IS", "NOT", "TRUE", "FALSE", "UNKNOWN", "NULL", //SIMILAR TO is allowed
        "EXISTS", "SINGULAR", "ALL", "ANY", "SOME", "HAVING", //IN is filtered below
        "INSERT", "DELETE", "DROP", "CREATE", "ALTER", "BEFORE", "AFTER", "NEW", ":", "EXEC", "DECLARE", //UPDATE is filtered below
        "FUNCTION", "MERGE", "USING", "UNION", "LIKE", "ORDER", "GROUP"
    );
    
    foreach($blacklist as $bad) {
        if(strpos($upperid, $bad) !== false) {
            die('{"status":"badword"}');
            exit();
        }
    }

    //allow FOR but not OR
    if (substr_count(str_replace('FOR', '***', $upperid), 'OR') > 0) {
        die('{"status":"badword"}');
        exit();
    }

    //allow SUBSTRING but not IN
    if (substr_count(str_replace('SUBSTRING', '***', $upperid), 'IN') > 0) {
        die('{"status":"badword"}');
        exit();
    }

    //allow RDB$UPDATE_FLAG but not UPDATE
    if (substr_count(str_replace('RDB$UPDATE_FLAG', '***', $upperid), 'UPDATE') > 0) {
        die('{"status":"badword"}');
        exit();
    }

    if (!($dbh = fbird_connect($host, $username, $password))) {
        $tab["errmsg"] = "DB connection error.";
    }
    $stmt = "SELECT * FROM SENTENCES WHERE ID = $id;";
    $sth = fbird_query($dbh, $stmt);
    while ($row = fbird_fetch_object($sth)) {
        $tab['status'] = 'ok';
        $tab['id'] = $row->ID;
        $tab['answer'] = $row->ANSWER;
    }
    if (!$tab["status"]) {
        $tab["status"] = "error";
    
    }
    echo json_encode($tab);
    
    fbird_free_result($sth);
    fbird_close($dbh);
}

?>
