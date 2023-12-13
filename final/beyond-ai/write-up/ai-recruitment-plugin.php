<?php
/**
* Plugin Name: Beyond Recruitment
* Plugin URI: http://beyond-ai.ecw
* Description: Recruitment plugin for Beyond AI
* Version: 1.0
* Author: Deborah
* Author URI: http://beyond-ai.ecw
**/

function recruitment_install () {
    global $wpdb;

    $table_name = $wpdb->prefix . "recruitment";
    $charset_collate = $wpdb->get_charset_collate();
    mkdir(plugin_dir_path(__FILE__) . "/ecw-beyond-ai-resumes");
    $sql = "CREATE TABLE $table_name (
        id mediumint(9) NOT NULL AUTO_INCREMENT,
        fullname text NOT NULL,
        email text NOT NULL,
        date DATE NOT NULL,
        resume text NOT NULL,
        seen boolean NOT NULL DEFAULT 0,
        PRIMARY KEY  (id)
    ) $charset_collate;";

    require_once( ABSPATH . 'wp-admin/includes/upgrade.php' );
    dbDelta( $sql );
}

function recruitment_uninstall () {
    global $wpdb;

    $table_name = $wpdb->prefix . "recruitment";
    system("rm -rf " . plugin_dir_path(__FILE__) . "/ecw-beyond-ai-resumes");
    $wpdb->query("DROP TABLE $table_name");
}

function create_endpoint() {
    add_rewrite_endpoint('ai-recruitment', EP_ROOT);
}

// to reach this page, go to "/?ai-recruitment"
function recruitment_page() {
    global $wp_query;
    global $wpdb;
    $to_print = '';
    if (isset($wp_query->query_vars['ai-recruitment'])) {
        echo '
    <!doctype html>
    <html>
        <head>
            <meta charset="UTF-8">
            <title>Beyond Recruitment Form</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body>
        ';
        // view applications
        if (isset($_GET['application'])) {
            $id = $_GET['application'];
            $to_print = '';
            $table_name = $wpdb->prefix . 'recruitment';
            if(isset($_POST['email']) && isset($_POST['fullname'])) {
                $email = stripslashes($_POST['email']);
                $fullname = stripslashes($_POST['fullname']);
                $query = "UPDATE $table_name SET email='" . $email . "', fullname='" . $fullname . "' WHERE id=$id";
                $wpdb->query( $query );
            }
            $application = $wpdb->get_row(
                $wpdb->prepare(
                    "
                        SELECT *
                        FROM  $table_name
                        WHERE id = %d
                    ",
                    $id
                )
            );
            $seen = 'No';
            $seen = $application->seen ? 'Yes' : 'No';
            echo $to_print;
            echo '
            <section class="bg-gray-50 dark:bg-gray-900">
                <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
                    <a href="#" class="flex items-center mb-6 text-2xl font-semibold text-gray-900 dark:text-white">
                    Application status
                    </a>
                    <div class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700">
                        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
                            <h1 class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                            Application number : ' . $application->id . '
                            </h1>
                            <form class="space-y-4 md:space-y-6" method="POST">
                                <div>
                                    <label for="email" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your email</label>
                                    <input value="' . $application->email . '" type="email" name="email" id="email" class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                                </div>
                                <div>
                                    <label for="fullname" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Fullname</label>
                                    <input value="' . $application->fullname . '" type="text" name="fullname" id="fullname"  class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                                </div>
                                <div>
                                    <label for="date" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Date</label>
                                    <input value="' . $application->date . '" type="text" id="date" class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" readonly>
                                </div>
                                <div>
                                    <label for="resume" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Resume</label>
                                    <input value="' . $application->resume . '" type="text" id="resume" class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" readonly>
                                </div>
                                <div>
                                    <label for="resume" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Seen</label>
                                    <input value="' . $seen . '" type="text" id="resume" class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" readonly>
                                </div>
                                <button type="submit" class="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800">Update informations</button>
                            </form>
                        </div>
                    </div>
                </div>
            </section>
        </body>
    </html>';
        exit;
        }

        // create application
        else if( isset($_POST['email']) && $_POST['email'] != '' &&
            isset($_POST['fullname']) && $_POST['fullname'] != '' &&
            isset($_FILES['resume'])) {

            $email = htmlspecialchars(trim($_POST['email']));
            $fullname = htmlspecialchars(trim($_POST['fullname']));
            $filename = htmlspecialchars(trim($_FILES["resume"]["name"]));
            $tempname = $_FILES["resume"]["tmp_name"];
            $mime_type = mime_content_type($tempname);
            $allowed_file_types = ['application/pdf'];
            if(!str_ends_with($filename, '.pdf') || !in_array($mime_type, $allowed_file_types)) {
                $to_print = '
                    <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                        <strong class="font-bold">Error</strong>
                        <span class="block sm:inline">File must be a PDF</span>
                        <span class="absolute top-0 bottom-0 right-0 px-4 py-3">
                            <svg class="fill-current h-6 w-6 text-red-500" role="button" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><title>Close</title><path d="M14.348 14.849a1.2 1.2 0 0 1-1.697 0L10 11.819l-2.651 3.029a1.2 1.2 0 1 1-1.697-1.697l2.758-3.15-2.759-3.152a1.2 1.2 0 1 1 1.697-1.697L10 8.183l2.651-3.031a1.2 1.2 0 1 1 1.697 1.697l-2.758 3.152 2.758 3.15a1.2 1.2 0 0 1 0 1.698z"/></svg>
                        </span>
                    </div>
                ';
            }
            else {
                $table_name = $wpdb->prefix . 'recruitment';
                $date = $wpdb->get_row(" SELECT DATE(NOW()) AS date");
                $wpdb->insert(
                    $table_name,
                    array(
                        'email' => $email,
                        'fullname' => $fullname,
                        'date' => $date->date,
                        'resume' => $filename,
                    )
                );

                $result = $wpdb->get_row ( "
                    SELECT id 
                    FROM  $table_name
                    ORDER BY id DESC
                    LIMIT 1
                " );
                $apply_directory = plugin_dir_path(__FILE__) . "/ecw-beyond-ai-resumes/" . $result->id;
                mkdir($apply_directory);
                move_uploaded_file($tempname, $apply_directory . "/" . $filename);
                $to_print = '
                    <div class="bg-indigo-900 text-center py-4 lg:px-4">
                        <div class="p-2 bg-indigo-800 items-center text-indigo-100 leading-none lg:rounded-full flex lg:inline-flex" role="alert">
                            <span class="flex rounded-full bg-indigo-500 uppercase px-2 py-1 text-xs font-bold mr-3">Success</span>
                            <span class="font-semibold mr-2 text-left flex-auto">You can view the status of your application <a href="http://beyond-ai.ecw/?ai-recruitment&application=' . $result->id . '" target="_blank">here</a></span>
                            <svg class="fill-current opacity-75 h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M12.95 10.707l.707-.707L8 4.343 6.586 5.757 10.828 10l-4.242 4.243L8 15.657l4.95-4.95z"/></svg>
                        </div>
                    </div>
                ';
            }
        }
        echo $to_print;
        echo '
        <section class="bg-gray-50 dark:bg-gray-900">
            <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
                <a href="#" class="flex items-center mb-6 text-2xl font-semibold text-gray-900 dark:text-white">
                Beyond AI    
                </a>
                <div class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700">
                    <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
                        <h1 class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                          Apply for a job
                        </h1>
                        <form class="space-y-4 md:space-y-6" method="POST" enctype="multipart/form-data">
                            <div>
                                <label for="email" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your email</label>
                                <input type="email" name="email" id="email" class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="name@company.com" required="">
                            </div>
                            <div>
                                <label for="fullname" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Fullname</label>
                                <input type="text" name="fullname" id="fullname" placeholder="Alice AI" class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required="">
                            </div>
                            <div>
                                <label for="resume" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Resume (PDF)</label>
                                <input type="file" name="resume" id="resume" class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required="">
                            </div>
                            <button type="submit" class="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800">Apply</button>
                        </form>
                    </div>
                </div>
            </div>
        </section>
    </body>
    </html>
        ';
        exit;
    }
}

function recruitment_flush_rewrite_rules() {
    flush_rewrite_rules();
}

register_activation_hook( __FILE__, 'recruitment_install' ); // update the DB schema
add_action('init', 'create_endpoint');
register_activation_hook(__FILE__, 'recruitment_flush_rewrite_rules');
register_uninstall_hook(__FILE__, 'recruitment_uninstall');
register_deactivation_hook(__FILE__, 'recruitment_uninstall');
add_action('template_redirect', 'recruitment_page');
