<?php
header('Content-Type: application/json');
$command = 'python "' . __DIR__ . '/../python/network.py"';
echo shell_exec($command);
?>