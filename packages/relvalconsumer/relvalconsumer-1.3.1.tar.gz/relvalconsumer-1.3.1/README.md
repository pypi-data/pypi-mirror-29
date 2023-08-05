# relvalconsumer

`relvalconsumer` is a fedmsg consumer for creating Fedora release validation
test events. It replaces the old `relval nightly --if-needed` sub-command,
which was expected to be run nightly as a cron job. Like the old system, each
time a compose appears, it runs various checks to decide whether it should
create an event for the compose. It creates events for both nightly composes
and 'candidate' composes.

It should create a first nightly for the next release shortly after a release
goes out. From then until the release, it will create new nightly events
periodically. It will never create a nightly event fewer than three days after
the current event. Between three and fourteen days after the current event,
it will create a new event if certain packages have changed (these are defined
in the code). After fourteen days it will create an event as soon as a nightly
compose appears. It will create events for all candidate composes as soon as
they appear.

It should never create an event for a given release from a Rawhide compose
after that release branches, because at that point wikitcms will decide that
any notional event for a Rawhide compose would be for the release *two* after
the current stable release, and this script will create events only for the
release *one* after the current stable release.

Note that in production mode the consumer is configured to create events in
the production wiki and send announcement emails to the test@ mailing list.
So, really, only one person should ever have it running in production mode,
and that's probably me. Please don't run it in production mode unless you're
taking over my job or something.

As long as relval is also installed, relvalconsumer will also run the image
size check on the newly-created event, whenever it creates an event.

The code was written with Python 3 in mind, but it turns out that verification
of fedmsg message signatures does not currently work in Python 3, so it should
be run under Python 2 for now.

## Requirements

Python libraries:

* [fedmsg](https://github.com/fedora-infra/fedmsg)
* [fedfind](https://pagure.io/fedora-qa/fedfind)
* [wikitcms](https://pagure.io/fedora-qa/python-wikitcms)
* [mwclient](https://github.com/mwclient/mwclient)

Optionally also [relval](https://pagure.io/fedora-qa/relval) itself, to run
image size check tests on the created events.

## Installation

Install the required external Python libraries, then use setuptools to
install, e.g.:

        python setup.py install

## Test and production modes

Two consumers are provided, a 'test' and a 'production' consumer. For 'test':

* The consumer listens for `dev` (not `prod`) messages
* The consumer does not validate message signatures
* The consumer creates events on the staging wiki (not production wiki)
* The announcement email is logged rather than being mailed out

In this mode it is fairly safe to play around with the consumer, and you can
use a tool like `fedmsg-dg-replay` to trigger event creation by replaying a
relevant fedmsg (which will show up with a `dev` topic rather than `prod`).

For 'production':

* The consumer listens for `prod` (not `dev`) messages
* The consumer validates message signatures
* **The consumer creates events on the production wiki**
* **The consumer sends email notifications to public mailing lists**

**PLEASE** do not enable the production consumer unless you're absolutely sure
it's your job to create the official events.

The fedmsg config keys for the consumers are `relvalconsumer.test.enabled`
and `relvalconsumer.prod.enabled` respectively.

## License

`relvalconsumer` is released under the [GPL](https://www.gnu.org/licenses/gpl.txt), version 3 or later. See `COPYING`
and the header of `relvalconsumer.py` itself.

## Contributing

Issues and pull requests can be filed in [Pagure](https://pagure.io/fedora-qa/relvalconsumer).
Pull requests must be signed off (use the `-s` git argument). By signing off
your pull request you are agreeing to the
[Developer's Certificate of Origin](http://developercertificate.org/):

    Developer's Certificate of Origin 1.1

    By making a contribution to this project, I certify that:

    (a) The contribution was created in whole or in part by me and I
        have the right to submit it under the open source license
        indicated in the file; or

    (b) The contribution is based upon previous work that, to the best
        of my knowledge, is covered under an appropriate open source
        license and I have the right under that license to submit that
        work with modifications, whether created in whole or in part
        by me, under the same open source license (unless I am
        permitted to submit under a different license), as indicated
        in the file; or

    (c) The contribution was provided directly to me by some other
        person who certified (a), (b) or (c) and I have not modified
        it.

    (d) I understand and agree that this project and the contribution
        are public and that a record of the contribution (including all
        personal information I submit with it, including my sign-off) is
        maintained indefinitely and may be redistributed consistent with
        this project or the open source license(s) involved.
