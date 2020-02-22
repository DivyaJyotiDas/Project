#!/bin/bash

#Cheecking the python verso


configure()
{
                #Logic for python cmd
                version=$(python --version 2>&1 | grep 3)
                result=$?
                python_cmd=""
                if [ $result -eq 0 && $version != "" ]
                then
                  echo"python command found"
                  python_cmd="python"
                fi


                #Logic for python3 cmd
                python3 --version
                result=$?
                version=$(python3 --version 2>&1 | grep 3)
                echo $result
                echo $version
                if [ $result -eq 0 && $version != "" && $python_cmd = "" ];
                then
                  echo "python3 command found"
                  python_cmd="python3"
                fi

                #Logic for python3.6 cmd
                #python3.6 --version
                result=$?
                version=$(python3.6 --version 2>&1 | grep 3)
                if [ $result -eq 0 && $version != "" && $python_cmd = "" ]
                then
                  echo "python 3.6 command found"
                  python_cmd="python3.6"
                fi

	exp_os=$(hostnamectl | grep Operating | cut -d':' -f2 | cut -b 2-7)
	echo $exp_os
	if [ "$exp_os" = "CentOS" ]
	then
                if [ $python_cmd == "" ]
                then
                   echo "Need to install python3.6"
                   sudo yum install -y https://centos7.iuscommunity.org/ius-release.rpm
                   if [ $? -eq 0 ]
                   then
                      echo "Configure the repository for installing the python 3.6"
                   else
                      echo "Not able to configure the yum repository for installing the python 3.6"
                      exit 0
                   fi
                   echo "Installing the python 3.6 in current machine."
                   sudo yum install -y python36u python36u-libs python36u-devel python36u-pip

                   if [ $? -eq 0 ]
                   then
                      echo "Python 3.6 installation completed"
                      python_cmd="python3.6"
                   else
                      echo "Some error occure while installing the  python 3.6, Please install the python 3.6 manualy and run this script again to install the package"
                      exit 0
                   fi
                   echo "Installing the python 3.6 in current machine."
                   echo



                fi

                #creating the python virtul environment

                #checke p://centos7.iuscommunity.org/ius-release.rpmthon3 folder present or not
                echo "creating python virual environment"

                if [ ! -f "python3" ];
                then
                   echo "Creating the python envionment in current directory"
                   echo $python_cmd
                   $python_cmd -m venv $(pwd)/apiexample/api_server_env
                   result=$?

                   echo "upgrading the python pip"
                   $python_cmd -m pip install --upgrade pip
                   if [ $result -eq 0 ]
                   then
                      echo "python3 virtual env created successfully"
                      echo "installing the requred package using requirment.txt"
                      source $(pwd)/apiexample/api_server_env/bin/activate
                      #value=$(python --version)
                      #echo $value
                      #/usr/local/bin/python -m pip install -r requirement.txt
                      $python_cmd -m pip install -r $(pwd)/apiexample/requirement.txt
                      #`$python_cmd -m pip install -r requirement.txt`
                      echo ""
                      echo "Activating the python virtual environment "
                      echo "source python3/bin/activate"
                      echo ""
                      echo "Starting the server"
                      echo "$python_cmd manage.py runserver <ip>:<port>"
                      $python_cmd $(pwd)/apiexample/manage.py runserver
                   fi

                fi
	elif [ "$exp_os" = "Ubuntu" ]
	then
		echo "HiiUbuntu"
		
		sudo add-apt-repository -y ppa:jonathonf/python-3.6
		sudo apt-get -y update
		sudo apt-get -y install python3.6
		sudo apt-get update
		sudo apt-get install python3.6

		sudo apt-get install python3-pip
		sudo pip3 install virtualenv
		virtualenv $(pwd)/apiexample/api_server_env
		source $(pwd)/apiexample/api_server_env/bin/activate

		python -m pip install -r $(pwd)/apiexample/requirements.txt
		python $(pwd)/apiexample/manage.py runserver
	else
		echo "OS Not Supported Yet"
	fi
}

run() {
        echo "running Server"
        echo "$2"
        source $(pwd)/apiexample/api_server_env/bin/activate
        $python_cmd $(pwd)/apiexample/manage.py runserver "$1"
}

echo "starting configure script"
if [ "$1" = 'configure' ]
then
        echo "configuring"
        configure
fi

if [ "$#" -ne 2 ]
then
        echo "Error <format> sh magic.sh run <ip>:<port>"

elif [ "$1" = "run" ]
then
        run "$2"
fi

