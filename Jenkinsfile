pipeline
{
	options
	{
		withAWS(endpointUrl:'https://s3.genpi64.com',credentials:'genpi-s3')
	}
	agent { node {
		label 'aarch64'
	} }
	stages { stage('Build') { matrix
	{
		agent any
		axes
		{
			axis
			{
				name 'INIT_SYSTEM'
				values 'OpenRC', 'Systemd'
			}
			axis
			{
				name 'LIBC'
				values 'GlibC'
			}
			axis
			{
				name 'ARCH'
				values 'aarch64'
			}
			axis
			{
				name 'LINK_TIME_OPTIMIZATION'
				values 'No'
			}
			axis
			{
				name 'GENTOO_HARDENED'
				values 'No'
			}
		}
		environment
		{
			PROJECT="GenPi64${INIT_SYSTEM}"
			BINPKGS_DIR="${HOME}/shared/binpkgs/"
			DISTFILES_DIR="${HOME}/shared/distfiles/"
			OVERLAYS_CACHE_DIR="${HOME}/shared/overlays-cache/"
			BINARY_ASSETS="${HOME}/shared/binary_assets/"
			NO_PARALLEL="yes"
			CHROOT_COMMAND="systemd-nspawn"
		}
		stages
		{
			stage('Clean Up') { steps
			{
				// Clear out anything from the previous build...
				sh "sudo rm -rf ./*"
				sh "git checkout ."
				sh "sudo rm -rf ${BINARY_ASSETS}"
			}}
			stage('Setup') { steps
			{
				sh "sudo mkdir -p $BINPKGS_DIR $DISTFILES_DIR $BINARY_ASSETS"
			}}
			stage('Print Environment') { steps
			{
				// Clear out anything from the previous build...
				sh "env"
				sh "ls -lah $BINPKGS_DIR"
				sh "ls -lah $DISTFILES_DIR"
				sh "ls -lah $BINARY_ASSETS"
			}}
			stage('Build Lite') { steps
			{
				// Here we want to only build the gentoo-base.json "subtarget"
				// but with the config for the selected init system, libc, and so on
				// since that has a big influence on the packages.
				sh "sudo --preserve-env ./build.sh"
			}}
			// matrix blocks cannot be nested inside other matrix blocks...
			//matrix
			//{
			//	agent any
			//	axes
			//	{
			//		axis
			//		{
			//			name 'PARTITION_TABLE'
			//			values 'msdos', 'hybrid', 'gpt'
			//		}
			//		axis
			//		{
			//			name 'BOOT_LOADER'
			//			values 'raspberrypi', 'grub', 'uefi', 'systemd-boot'
			//		}
			//		axis
			//		{
			//			name 'INITRAMFS'
			//			values 'None', 'dracut', 'raspberrypi-initramfs'
			//		}
			//	}
			//	stages
			//	{
			stage('Package Lite') { steps
			{
				// Here we resume from the end of gentoo-base.json
				// and want to launch one job per partition table scheme
				// since the on-disk format will be different for each scheme
				// we want to use btrfs subvolume snapshotting to give each
				// partition type it's own build workspace.
				// there *should* be a way to make jenkins dynamically schedule
				// a single dimensional matrix of jobs to accomplish this
				// so that the runner is fully occupied.
				echo "Package Lite"
			}}
			stage('Upload Lite') { steps
			{
				s3Upload(bucket:"images", includePathPattern:'*.zst')
			}}
				//}
			//}

			stage('Build Desktop')
			{
				environment
				{
					PROJECT="GenPi64${INIT_SYSTEM}Desktop"
				}
				steps
				{
					// Here we need to spawn a matrix of jobs that starts from
					// the gentoo-base.json for the current init system, libc, and so on
					// and produces an image for each desktop varient we offer.
					// E.g. xfce, lxqt, so on.
					sh "sudo --preserve-env ./build.sh"
				}
			}
			stage('Package Desktop') { steps
			{
				// here we resume from the end of the desktop job and produce an image
				// file for each desktop job for each partition type. Ultimately
				// producing a matrix of a matrix of a matrix of images.
				// we have 5 matrix diminsions for the base image(arch, libc, init, lto, hardened)
				// then some number of desktop environments (xfce, lxqt, gnome, kde, so on)
				// then 3 potential partition schemes (msdos, hybrid, gpt)
				// then 4 potential bootloaders (raspi native (excluded from x86), uefi "native", grub, systemd-boot)
				// ultimately culminating in an 8 dimensional matrix of images that we can produce.
				// though of course there are big holes in the matrix, and we would only produce images
				// that someone is willing to put work into.
				echo "Package Desktop"
			}}
			stage('Upload Desktop') { steps
			{
				s3Upload(bucket:"images", includePathPattern:'*.zst')
			}}
		}
		post { always
		{
			sh "sudo rm -rf ./*"
		}}
	}}}
}