## Prerequisites
install Py3.4.x

## Configuration
edit 'ngs/init.cfg'
For example,

	[urls]
	# for dev append :9080
	base_dir: http://localhost:9080


## Install
sudo python3 setup.py install


## Run
go to 'scripts' and then run the batch_export.py.
For example:

	python3 batch_export.py -u converge@hid.com -p Converge@123  -b Batch-1004 -o test1.csv



