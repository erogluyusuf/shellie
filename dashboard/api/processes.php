<?php
header('Content-Type: application/json');
$command = 'python "' . __DIR__ . '/../python/processes.py"';
echo shell_exec($command);
?>