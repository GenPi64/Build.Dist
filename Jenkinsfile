pipeline {
	agent { label 'aarch64' }

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
		// Initial cleanup and setup (runs in main workspace)
		stage('Initial Setup') {
			agent { label 'aarch64' }
			steps {
				sh "cat /proc/mounts"

				sh "for var in ./build/*/image/*; do sudo umount -lfd \$var || sudo umount -ld \$var || sudo umount -l \$var ||  echo \"\$var not a mount point\"; done"
				sh "for var in ./build/*/*; do sudo umount -lfd \$var || sudo umount -ld \$var || sudo umount -l \$var ||  echo \"\$var not a mount point\"; done"

				sh "sudo losetup -all --list --output NAME,BACK-FILE"
				sh "for var in \$(sudo losetup -all --list --output NAME,BACK-FILE | grep deleted | cut -f1 -d' '); do losetup -d \$var || echo \"\$(sudo losetup -all --list --output NAME,BACK-FILE | grep \$var) cant be detached\"; done"
				sh "sudo losetup -D"

				sh "sudo rm -rf ./*"
				sh "git checkout ."
				sh "sudo mkdir -p $CCACHE_DIR $BINPKGS_DIR $DISTFILES_DIR $BINARY_ASSETS $OVERLAYS_CACHE_DIR"
			}
		}

		stage('Print Environment'){
			agent { label 'aarch64' }
			steps {
			// Clear out anything from the previous build...
			sh "env"
			sh "ls -lah  $CCACHE_DIR"
			sh "ls -lahR $BINPKGS_DIR"
			sh "ls -lahR $DISTFILES_DIR"
			sh "ls -lahR $BINARY_ASSETS"
			// Will kill the build if doesn't exist otherwise..
			sh "ls -lah  $OVERLAYS_CACHE_DIR"
		}}

		// Base images - each gets its own native workspace (@1, @2, etc.)
		stage('Build Base Images') {
			matrix {
				axes {
					axis {
						name 'INIT_SYSTEM'
						values 'OpenRC', 'Systemd', 'Osuosl'
					}
				}
				stages {
					stage('Build') {
						agent {
							label 'aarch64'
							// Jenkins will automatically assign @1, @2, etc.
						}
						steps {
							script {
								// Fresh checkout in this workspace
								checkout scm

								def project = "GenPi64${INIT_SYSTEM}"
								echo "Building ${project} base in workspace ${env.WORKSPACE}"
								buildProject(project)
							}
						}
					}
				}
			}
		}
		// Desktop images - each gets its own native workspace
		stage('Build Desktop Images') {
			matrix {
				axes {
					axis {
						name 'INIT_SYSTEM'
						values 'OpenRC', 'Systemd'
					}
				}
				stages {
					stage('Build') {
						agent {
							label 'aarch64'
							// Jenkins will automatically assign @3, @4, etc.
						}
						steps {
							script {
								// Fresh checkout in this workspace
								checkout scm

								def project = "GenPi64${INIT_SYSTEM}Desktop"
								echo "Building ${project} in workspace ${env.WORKSPACE}"
								buildProject(project)
							}
						}
					}
				}
			}
		}



        stage('Upload Artifacts') {
			agent { label 'aarch64' }
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
		stage('Upload binary packages') {
			agent { label 'aarch64' }
			environment {
				BINPKGS_DIR="${HOME}/shared/binpkgs"
			}
			steps {
				sh "ls -lah ${BINPKGS_DIR}"
				minio(bucket:"binpkgs", includes:"${BINPKGS_DIR}/**")
			}
		}
	}

    post {
        always {
            script {
                // Cleanup with retries
                echo "Cleaning up..."
				// Clear out anything from the previous build...
				sh "cat /proc/mounts"

				sh "for var in ./build/*/image/*; do sudo umount -lfd \$var || sudo umount -ld \$var || sudo umount -l \$var ||  echo \"\$var not a mount point\"; done"
				sh "for var in ./build/*/*; do sudo umount -lfd \$var || sudo umount -ld \$var || sudo umount -l \$var ||  echo \"\$var not a mount point\"; done"

				sh "for var in \$(find . -maxdepth 1 -name './build/*/chroot/var/log/emerge.log' -print); do sudo cat \$var; done"

				sh "sudo losetup -all --list --output NAME,BACK-FILE"
				sh "for var in \$(sudo losetup -all --list --output NAME,BACK-FILE | grep deleted | cut -f1 -d' '); do losetup -d \$var || echo \"\$(sudo losetup -all --list --output NAME,BACK-FILE | grep \$var) cant be detached\"; done"
				sh "sudo losetup -D"
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

	sh "sudo --preserve-env ./.ci/scripts/check-filename-is-renamed.sh"

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
