<?php
error_reporting(0);
ini_set('display_errors', 0);
header('Content-Type: application/json');

// Include database configuration
require_once 'config.php';

// If connection failed, config.php already returned JSON error
if (!isset($conn)) {
    exit;
}

// Check if form is submitted
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get form data
    $name = trim($_POST['name'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $password = $_POST['password'] ?? '';
    $confirmPassword = $_POST['confirmPassword'] ?? '';
    $disability = $_POST['disability'] ?? '';

    // Validate inputs
    if (empty($name) || empty($email) || empty($password) || empty($disability)) {
        echo json_encode(['success' => false, 'message' => 'All fields are required']);
        exit;
    }

    if ($password !== $confirmPassword) {
        echo json_encode(['success' => false, 'message' => 'Passwords do not match']);
        exit;
    }

    if (strlen($password) < 6) {
        echo json_encode(['success' => false, 'message' => 'Password must be at least 6 characters']);
        exit;
    }

    // Check if email already exists
    $checkEmail = $conn->prepare("SELECT id FROM users WHERE email = ?");
    $checkEmail->bind_param("s", $email);
    $checkEmail->execute();
    $result = $checkEmail->get_result();

    if ($result->num_rows > 0) {
        echo json_encode(['success' => false, 'message' => 'Email already registered']);
        exit;
    }

    // Hash password
    $hashedPassword = password_hash($password, PASSWORD_DEFAULT);

    // Insert user into database
    $stmt = $conn->prepare("INSERT INTO users (name, email, password, disability) VALUES (?, ?, ?, ?)");
    $stmt->bind_param("ssss", $name, $email, $hashedPassword, $disability);

    if ($stmt->execute()) {
        echo json_encode(['success' => true, 'message' => 'Account created successfully', 'disability' => $disability]);
    } else {
        echo json_encode(['success' => false, 'message' => 'Error creating account: ' . $stmt->error]);
    }

    $stmt->close();
    $checkEmail->close();
} else {
    echo json_encode(['success' => false, 'message' => 'Invalid request method']);
}

$conn->close();
?>
