pipeline {
    agent {
        label 'Blender Node'
    }
    stages {
        stage('Checkout from GitHub') {
            steps {
                script {
                    checkout([$class: 'GitSCM', branches: [[name: 'main']], userRemoteConfigs: [[url: 'https://github.com/glcooke/blender_trial_task']]])
                }
            }
        }
        stage('Run Scripts') {
            steps {
                script {
                    def blender_path = params.blender_path
                    def output_path = params.output_path
                    def x_resolution = params.x_resolution
                    def y_resolution = params.y_resolution
                }
                dir (output_path.substring(1, output_path.length() - 1)) {
                    deleteDir()
                }
                withPythonEnv("${WORKSPACE}\\python\\python.exe") {
                    bat '''
                        pip install -r requirements.txt
                        cd test
                        python main.py %blender_path% %output_path% %x_resolution% %y_resolution%
                    '''

                }
            }
        }
        stage('Archive') {
            steps {
                dir(output_path.substring(1, output_path.length() - 1)) {
                    archiveArtifacts artifacts: '**', allowEmptyArchive: true
                }
            }
        }
    }
}