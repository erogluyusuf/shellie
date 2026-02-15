<?php

$action = $_GET["action"] ?? "";

if ($action == "kill") {
    $pid = intval($_GET["pid"]);
    echo shell_exec("taskkill /PID $pid /F");
}

if ($action == "flush_dns") {
    echo shell_exec("ipconfig /flushdns");
}
