pipeline {
    agent {
        node {
            label 'aarch64'
        }
    }

    options {
        timestamps()
        skipDefaultCheckout(true)
    }

    environment {
        // Shared directories
        SHARED_DIR = "/home/jenkins/shared"
        CCACHE_DIR = "${SHARED_DIR}/ccache"
        BINPKGS_DIR = "${SHARED_DIR}/binpkgs"
        OVERLAYS_CACHE_DIR = "${SHARED_DIR}/overlays-cache"
        BUILD_DIR = "${WORKSPACE}/build"

        // Build configuration
        INIT_SYSTEMS = ['OpenRC', 'Systemd']
        BUILDVERSION = sh(script: 'date +%d-%m-%y', returnStdout: true).trim()
        SUDO_CMD = "sudo -E"

        // MinIO configuration (should match your Jenkins credentials)
        MINIO_BUCKET = "images"
    }

    stages {
        stage('Prepare Environment') {
            steps {
                script {
                    sh """
                        mkdir -p ${CCACHE_DIR} ${BINPKGS_DIR} ${OVERLAYS_CACHE_DIR}
                        chmod -R 755 ${SHARED_DIR}
                        chown -R jenkins:jenkins ${SHARED_DIR}
                    """
                }
            }
        }

        stage('Update Repositories') {
            steps {
                script {
                    // Update Gentoo repo
                    dir("${OVERLAYS_CACHE_DIR}/var/db/repos/gentoo") {
                        sh '''
                            if [ -d .git ]; then
                                git pull
                            else
                                git clone https://github.com/gentoo-mirror/gentoo.git .
                            fi
                        '''
                    }

                    // Update GenPi64 overlay
                    dir("${OVERLAYS_CACHE_DIR}/var/db/repos/genpi64") {
                        sh '''
                            if [ -d .git ]; then
                                git pull
                            else
                                git clone https://github.com/GenPi64/genpi64-overlay.git .
                            fi
                        '''
                    }
                }
            }
        }

        stage('Build Images') {
            steps {
                script {
                    // Build base and desktop images for each init system
                    for (initSystem in INIT_SYSTEMS) {
                        def baseProject = "GenPi64${initSystem}"
                        def desktopProject = "${baseProject}Desktop"

                        echo "Building ${baseProject}..."
                        buildProject(baseProject)

                        echo "Building ${desktopProject}..."
                        buildProject(desktopProject)
                    }
                }
            }
        }

        stage('Upload Artifacts') {
            steps {
                script {
                    // Upload all built images using MinIO plugin
                    def allProjects = []
                    for (initSystem in INIT_SYSTEMS) {
                        allProjects.add("GenPi64${initSystem}")
                        allProjects.add("GenPi64${initSystem}Desktop")
                    }

                    for (project in allProjects) {
                        uploadArtifacts(project)
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                // Cleanup with retries
                echo "Cleaning up..."
                sh """
                    for i in {1..3}; do
                        ${SUDO_CMD} umount -R ${BUILD_DIR}/* 2>/dev/null || true
                        ${SUDO_CMD} losetup -D || true
                        sleep 2
                    done
                """
            }
        }

        success {
            echo "Build completed successfully!"
        }

        failure {
            echo "Build failed! Check logs for details."
        }
    }
}

// Helper function to build a project
def buildProject(project) {
    def envVars = [
        "PROJECT=${project}",
        "CCACHE_DIR=${CCACHE_DIR}",
        "BINPKGS_DIR=${BINPKGS_DIR}",
        "OVERLAYS_CACHE_DIR=${OVERLAYS_CACHE_DIR}",
        "BUILDVERSION=${BUILDVERSION}",
        "WORKSPACE=${WORKSPACE}"
    ].join(' ')

    sh "${envVars} ${SUDO_CMD} ${WORKSPACE}/build.sh"
}

// Helper function to upload artifacts using MinIO plugin
def uploadArtifacts(project) {
    def artifacts = [
        "${project}-${BUILDVERSION}.img.zst",
        "${project}-${BUILDVERSION}.tar.zst",
        "${project}-${BUILDVERSION}.img.zst.sum"
    ]

    for (artifact in artifacts) {
        def fullPath = "${BUILD_DIR}/${project}/${artifact}"
        if (fileExists(fullPath)) {
            echo "Uploading ${artifact} to MinIO..."
            minio(
                bucket: env.MINIO_BUCKET,
                includes: fullPath
            )
        } else {
            echo "Warning: Artifact ${fullPath} not found"
        }
    }
}
