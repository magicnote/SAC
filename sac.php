<?php

if (1 == $argc) {
    notfound();
}

$vendor = 'vendor/autoload.php';

if (isset($argv[2])) {
    $vendor = trim($argv[2], ' \\') . '\\' . $vendor;
}
 
require $vendor;
 
$cls = '\\' . trim($argv[1], ' \\');

try {
    $reflection = new \ReflectionClass($cls);
    print_r(json_encode(array_map(function ($item) {
        return $item->name;
    }, $reflection->getMethods())));
} catch (\Exception $e) {
    notfound();
}

function notfound()
{
    print_r('[]');
    die();
}
