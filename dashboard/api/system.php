<?php
header('Content-Type: application/json');
// Python dosyasının tam yolu (Windows için ters eğik çizgiye dikkat etmeyebiliriz ama garanti olsun diye __DIR__)
$command = 'python "' . __DIR__ . '/../python/system.py"';
$output = shell_exec($command);
echo $output;
?>