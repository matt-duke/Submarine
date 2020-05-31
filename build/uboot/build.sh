cat << EOF > boot.cmd
	fdt addr \${fdt_addr} && fdt get value bootargs /chosen bootargs
	fatload mmc 0:1 \${kernel_addr_r} uImage
	bootm \${kernel_addr_r} - \${fdt_addr}
EOF
mkimage -A arm -T script -C none -n "Boot script" -d "boot.cmd" boot.scr

mkimage -A arm -O linux -T kernel -C none -a 0x00008000 -e 0x00008000 -n "Linux kernel" -d /run/media/me/boot/$KERNEL /run/media/me/boot/uImage