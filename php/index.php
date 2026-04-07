<?php
require_once "db.php";

$messages = [];

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $user_input = trim($_POST["message"] ?? "");

    if ($user_input !== "") {
        // apelăm API-ul Flask
        $payload = json_encode(["message" => $user_input]);

        $ch = curl_init("http://127.0.0.1:5000/chat");
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
        curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            "Content-Type: application/json",
            "Content-Length: " . strlen($payload)
        ]);

        $response = curl_exec($ch);
        curl_close($ch);

        if ($response !== false) {
            $data = json_decode($response, true);
            if (isset($data["messages"])) {
                $messages = $data["messages"];

                // ultimul mesaj de la asistent
                $bot_reply = "";
                foreach (array_reverse($messages) as $m) {
                    if ($m["role"] === "assistant") {
                        $bot_reply = $m["content"];
                        break;
                    }
                }

                // salvăm în DB
                $stmt = $pdo->prepare("INSERT INTO chat_history (user_input, bot_reply) VALUES (?, ?)");
                $stmt->execute([$user_input, $bot_reply]);
            }
        }
    }
}

// încărcăm istoricul
$stmt = $pdo->query("SELECT * FROM chat_history ORDER BY created_at DESC LIMIT 20");
$history = $stmt->fetchAll();
?>
<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <title>Chatbot Anca + Google Drive</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 900px; margin: 20px auto; }
        .chat-box { border: 1px solid #ccc; padding: 10px; margin-bottom: 20px; max-height: 300px; overflow-y: auto; }
        .msg-user { color: #004085; margin-bottom: 5px; }
        .msg-bot { color: #155724; margin-bottom: 10px; }
        .history { margin-top: 30px; }
        textarea { width: 100%; height: 80px; }
        button { padding: 8px 16px; }
    </style>
</head>
<body>
<h1>Chatbot Anca + Google Drive</h1>

<form method="post">
    <label for="message">Întrebarea ta:</label><br>
    <textarea name="message" id="message" required></textarea><br><br>
    <button type="submit">Trimite</button>
</form>

<?php if (!empty($messages)): ?>
    <h2>Ultima conversație</h2>
    <div class="chat-box">
        <?php foreach ($messages as $m): ?>
            <?php if ($m["role"] === "user"): ?>
                <div class="msg-user"><strong>Tu:</strong> <?= htmlspecialchars($m["content"]) ?></div>
            <?php elseif ($m["role"] === "assistant"): ?>
                <div class="msg-bot"><strong>Chatbot:</strong> <?= nl2br(htmlspecialchars($m["content"])) ?></div>
            <?php endif; ?>
        <?php endforeach; ?>
    </div>
<?php endif; ?>

<div class="history">
    <h2>Istoric ultimele 20 de întrebări</h2>
    <?php foreach ($history as $row): ?>
        <div style="margin-bottom: 15px;">
            <div><strong>Tu:</strong> <?= htmlspecialchars($row["user_input"]) ?></div>
            <div><strong>Chatbot:</strong> <?= nl2br(htmlspecialchars($row["bot_reply"])) ?></div>
            <small><?= $row["created_at"] ?></small>
        </div>
    <?php endforeach; ?>
</div>

</body>
</html>
