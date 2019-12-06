# Download repos list
ROOT=$(pwd)

gerrit_url=$1

for repo in $(curl ${gerrit_url}/r/projects/?format=text); do

  echo $repo
  flat_name=$(echo $repo |sed -e 's/\//_/g')

  if [ ! -d $ROOT/repos/$flat_name ]; then
      echo "Cloning $repo from $gerrit_url/r/$repo $ROOT/repos/$flat_name"
      git clone $gerrit_url/r/$repo $ROOT/repos/$flat_name
  else
      cd $ROOT/repos/$flat_name
      echo "Updating $repo"
      git checkout $branch && git fetch --all && git pull
      cd $ROOT
  fi;

done
