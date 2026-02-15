<?php
header('Content-Type: application/json');
echo shell_exec("python ../python/services.py");
