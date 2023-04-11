<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

// Replace these values with your own database credentials
$db_host = 'localhost';
$db_user = 'your_db_user';
$db_password = 'your_db_password';
$db_name = 'your_db_name';

$connection = new mysqli($db_host, $db_user, $db_password, $db_name);

if ($connection->connect_error) {
  http_response_code(500);
  die(json_encode(['error' => 'Failed to connect to the database']));
}

switch ($_SERVER['REQUEST_METHOD']) {
  case 'GET':
    // If an ID is provided, get a specific guitar, otherwise list all guitars
    $id = isset($_GET['id']) ? intval($_GET['id']) : null;
    if ($id) {
      $stmt = $connection->prepare('SELECT * FROM guitars WHERE id = ?');
      $stmt->bind_param('i', $id);
    } else {
      $stmt = $connection->prepare('SELECT * FROM guitars');
    }

    $stmt->execute();
    $result = $stmt->get_result();
    $guitars = $result->fetch_all(MYSQLI_ASSOC);
    echo json_encode($id ? $guitars[0] : $guitars);
    break;

  case 'POST':
    // Insert a new guitar
    $data = json_decode(file_get_contents('php://input'), true);
    $stmt = $connection->prepare('INSERT INTO guitars (make, model, year, color) VALUES (?, ?, ?, ?)');
    $stmt->bind_param('ssis', $data['make'], $data['model'], $data['year'], $data['color']);
    $stmt->execute();
    $id = $connection->insert_id;
    header('Location: /api.php?id=' . $id, true, 201);
    echo json_encode(['id' => $id]);
    break;

  case 'PUT':
    // Update an existing guitar
    $id = isset($_GET['id']) ? intval($_GET['id']) : null;
    if (!$id) {
      http_response_code(400);
      die(json_encode(['error' => 'Missing guitar ID']));
    }

    $data = json_decode(file_get_contents('php://input'), true);
    $stmt = $connection->prepare('UPDATE guitars SET make = ?, model = ?, year = ?, color = ? WHERE id = ?');
    $stmt->bind_param('ssisi', $data['make'], $data['model'], $data['year'], $data['color'], $id);
    $stmt->execute();
    echo json_encode(['id' => $id]);
    break;

  case 'DELETE':
    // Delete a guitar
    $id = isset($_GET['id']) ? intval($_GET['id']) : null;
    if (!$id) {
      http_response_code(400);
      die(json_encode(['error' => 'Missing guitar ID']));
    }

    $stmt = $connection->prepare('DELETE FROM guitars WHERE id = ?');
    $stmt->bind_param('i', $id);
    $stmt->execute();
    echo json_encode(['id' => $id]);
    break;

  default:
    http_response_code(405);
    die(json_encode(['error' => 'Invalid request method']));
}

$connection->close();

