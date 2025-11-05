pipeline {
    agent {
        node {
            label 'aarch64'
        }
    }

    options {
        timestamps()
    }

    environment {
        // Shared directories
        SHARED_DIR = "/home/jenkins/shared"
        CCACHE_DIR = "${SHARED_DIR}/ccache"
        BINPKGS_DIR = "${SHARED_DIR}/binpkgs"
		DISTFILES_DIR="${SHARED_DIR}/distfiles"
		BINARY_ASSETS="${SHARED_DIR}/binary_assets"
        OVERLAYS_CACHE_DIR = "${SHARED_DIR}/overlays-cache"
        BUILD_DIR = "${WORKSPACE}/build"
		NO_PARALLEL="yes"

        // Build configuration
        INIT_SYSTEMS_STR = "OpenRC,Systemd"
        BUILDVERSION = sh(script: "date +%d-%m-%y", returnStdout: true).trim()
        SUDO_CMD = "sudo -E"

        // MinIO configuration (should match your Jenkins credentials)
        MINIO_BUCKET = "images"
    }

    stages {
        stage('Prepare Environment') {
            steps {
                script {
                    sh """
                        mkdir -p ${CCACHE_DIR} ${DISTFILES_DIR} ${BINARY_ASSETS} ${BINPKGS_DIR} ${OVERLAYS_CACHE_DIR} 
                        ${SUDO_CMD} chmod -R 755 ${SHARED_DIR}
                        ${SUDO_CMD} chown -R jenkins:jenkins ${SHARED_DIR}
                    """
                }
            }
        }

		stage('Print Environment') { steps
		{
			// Clear out anything from the previous build...
			sh "env"
			sh "ls -lah  $CCACHE_DIR"
			sh "ls -lahR $BINPKGS_DIR"
			sh "ls -lahR $DISTFILES_DIR"
			sh "ls -lahR $BINARY_ASSETS"
			// Will kill the build if doesn't exist otherwise..
			sh "ls -lah  $OVERLAYS_CACHE_DIR"
		}}

		stage('Build Base Images') {
			matrix {
				axes {
					axis {
						name 'INIT_SYSTEM'
						values 'OpenRC', 'Systemd', 'Osuosl'
					}
				}
				stages {
					stage('Build Base') {
						steps {
							script {
								def project = "GenPi64${INIT_SYSTEM}"
								echo "Building ${project}..."
								buildProject(project)
							}
						}
					}
				}
			}
		}

		stage('Build Desktop Images') {
			matrix {
				axes {
					axis {
						name 'INIT_SYSTEM'
						values 'OpenRC', 'Systemd'
					}
				}
				stages {
					stage('Build Desktop') {
						steps {
							script {
								def project = "GenPi64${INIT_SYSTEM}Desktop"
								echo "Building ${project}..."
								buildProject(project)
							}
						}
					}
				}
			}
		}

        stage('Upload Artifacts') {
            steps {
                script {
					def initSystems = ['OpenRC', 'Systemd', 'Osuosl']
					def variants = ['', 'Desktop']

					for (initSystem in initSystems) {
						if (initSystem == 'Osuosl') {
							variants = [''] // Osuosl has no variants
						} else {
							variants = ['', 'Desktop']
						}
						for (variant in variants) {
							def project = "GenPi64${initSystem}${variant}"
							uploadArtifacts(project)
						}
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
