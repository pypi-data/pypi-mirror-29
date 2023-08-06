# Python Wrapper for AWS Batch use at Fred Hutch

This wrapper enables secure use from Python of AWS Batch
at Fred Hutch and works around some
[security issues](https://forums.aws.amazon.com/thread.jspa?threadID=270071&tstart=0)
related to submission and termination of jobs.

You only use this wrapper if you are interacting with AWS Batch via
Python (that is, you are using the `boto3` package).
If you are interacting with AWS Batch via the command line,
use the standalone
[command-line wrapper](https://github.com/FredHutch/batch-wrapper-client-golang).

For the most part, you use AWS Batch as you normally would, as explained in its
[documentation](https://aws.amazon.com/documentation/batch/)
and the [Fred Hutch Batch documentation](https://fredhutch.github.io/aws-batch-at-hutch-docs/).

The only difference (explained below) is when you want to submit a job,
or terminate/cancel a job.

## Installation

First, use a version of Python 3:

```
ml Python/3.6.4-foss-2016b-fh1
```

Now, install the package:

```
pip install fredhutch_batch_wrapper --user
```

(If you are using a [virtual environment](https://docs.python.org/3/tutorial/venv.html),
you can omit the `--user`).


### AWS Credentials

If you haven't already, please [obtain your AWS credentials](https://teams.fhcrc.org/sites/citwiki/SciComp/Pages/Getting%20AWS%20Credentials.aspx) and
[request access](https://fredhutch.github.io/aws-batch-at-hutch-docs/#request-access) to AWS Batch before proceeding further.
AWS credentials (and Batch onboarding) are required before this
Batch wrapper will work.

## Usage

Make sure you are using the appropriate
version of Python, in which you have previously installed the wrapper.
Be sure to run

```
ml Python/3.6.4-foss-2016b-fh1
```

before working with the wrapper.


Using the wrapper is very similar to using the
[batch client](https://boto3.readthedocs.io/en/latest/reference/services/batch.html#client)
in `boto3`. In fact, you will continue to use `boto3` for everything
except submitting, terminating, and canceling jobs.

In order to use the wrapper, you must first create a client:

```python
import fredhutch_batch_wrapper

client = fredhutch_batch_wrapper.get_client()
```

The `client` object has three methods: `submit_job()`, `cancel_job()`,
and `terminate_job()`. They take exactly the same arguments
(and return the same values)
as their
counterparts in `boto3`:

* [submit_job()](https://boto3.readthedocs.io/en/latest/reference/services/batch.html#Batch.Client.submit_job)
* [cancel_job()](https://boto3.readthedocs.io/en/latest/reference/services/batch.html#Batch.Client.cancel_job)
* [terminate_job()](https://boto3.readthedocs.io/en/latest/reference/services/batch.html#Batch.Client.terminate_job)

## More Information

* [boto3 Batch Documentation](https://boto3.readthedocs.io/en/latest/reference/services/batch.html#client)
* [Using AWS Batch at Fred Hutch](https://fredhutch.github.io/aws-batch-at-hutch-docs/)
* [Getting AWS Credentials](https://teams.fhcrc.org/sites/citwiki/SciComp/Pages/Getting%20AWS%20Credentials.aspx)

If you have further questions, please contact
[SciComp](https://centernet.fredhutch.org/cn/u/center-it/cio/scicomp.html).
