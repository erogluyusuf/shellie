<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Shellie Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f4f4f9;
            display: flex;
            justify_content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .card {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            text-align: center;
        }
        h1 { color: #333; }
        p { color: #666; }
    </style>
</head>
<body>
    <div class="card">
        <h1>👋 Hoşgeldin Patron!</h1>
        <p>Burası senin PHP tabanlı kontrol panelin.</p>
        <p style="font-size: 12px; color: #999;">Sistem: <?php echo php_uname(); ?></p>
    </div>
</body>
</html>