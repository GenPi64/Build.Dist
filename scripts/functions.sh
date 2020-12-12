

ckmkdir () {

if [[ ! -d "$1" ]]; then
  if [[ ! -e "$1" ]]; then
    mkdir -p "$1"
  fi
fi

}

copyconf () {

pushd `dirname $0`

if [[ -z "$2" ]]; then
  U="root"
else
  U="$2"
fi


if [[ -z "$3" ]]; then
  G="root"
else
  G=$3
fi


for ITEM in $(ls $PROJECT); do
  if [[ -d "$PROJECT/$ITEM" ]]; then
    mkdir -p $PROJECT_DIR/chroot/$1/${ITEM}
    for ITEM2 in $(ls ${PROJECT}/${ITEM}/); do
      cp -r $PROJECT/$ITEM/$ITEM2 $PROJECT_DIR/chroot/$1/$ITEM/$ITEM2
      chown $U:$G $PROJECT_DIR/chroot/$1/${ITEM}/$ITEM2
    done
  else
    cp -r ${PROJECT}/${ITEM} $PROJECT_DIR/chroot/$1/${ITEM}
    chown $U:$G $PROJECT_DIR/chroot/$1/${ITEM}
  fi
done


popd

}
