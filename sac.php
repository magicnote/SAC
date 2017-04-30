<?php
require 'vendor/autoload.php';

if (1 == $argc) {
    notfound();
}

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
