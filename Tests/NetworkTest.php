<?php

namespace Remotelabz\NetworkBundle\Tests;

use PHPUnit\Framework\TestCase;
use Remotelabz\NetworkBundle\Entity\IP;
use Remotelabz\NetworkBundle\Entity\Network;
use Remotelabz\NetworkBundle\Exception\BadNetmaskException;

class NetworkTest extends TestCase
{
    public function testGetId()
    {
        $network = new Network("10.0.0.0", "255.0.0.0");
        $this->assertEquals(null, $network->getId());
    }

    public function testSetIp()
    {
        $network = new Network("10.0.0.0", "255.0.0.0");

        $expected = new IP("127.0.0.30");

        $network->setIp($expected);
        $this->assertEquals($expected, $network->getIp());
    }

    public function testSetNetmask()
    {
        $network = new Network("10.0.0.0", "255.0.0.0");

        $expected = new IP("255.255.255.0");

        $network->setNetmask($expected);
        $this->assertEquals($expected, $network->getNetmask());
    }

    public function testGetFirstIP()
    {
        $network = new Network("127.0.0.16", "255.255.255.240");

        $expected = new IP("127.0.0.17");

        $first = $network->getFirstAddress();
        $this->assertEquals($expected, $first);
    }

    public function testGetLastIP()
    {
        $network = new Network("127.0.0.16", "255.255.255.240");

        $expected = new IP("127.0.0.30");

        $first = $network->getLastAddress();
        $this->assertEquals($expected, $first);
    }

    public function testGetIpRange()
    {
        // 127.0.0.16/28
        $network = new Network("127.0.0.16", "255.255.255.240");

        $expected = [
            "127.0.0.17",
            "127.0.0.18",
            "127.0.0.19",
            "127.0.0.20",
            "127.0.0.21",
            "127.0.0.22",
            "127.0.0.23",
            "127.0.0.24",
            "127.0.0.25",
            "127.0.0.26",
            "127.0.0.27",
            "127.0.0.28",
            "127.0.0.29",
            "127.0.0.30"
        ];

        $range = $network->getAllIp();
        $this->assertEquals($expected, $range, 'IP range doesn\'t match.');

        // 127.0.0.16/28, exclude "127.0.0.24" & "127.0.0.28"
        $network = new Network("127.0.0.16", "255.255.255.240");

        $expected = [
            "127.0.0.17",
            "127.0.0.18",
            "127.0.0.19",
            "127.0.0.20",
            "127.0.0.21",
            "127.0.0.22",
            "127.0.0.23",
            "127.0.0.25",
            "127.0.0.26",
            "127.0.0.27",
            "127.0.0.29",
            "127.0.0.30"
        ];

        $range = $network->getAllIp([new IP("127.0.0.24"), new IP("127.0.0.28")]);
        $this->assertEquals($expected, $range, 'IP range doesn\'t match.');

        // 127.0.0.16/30
        $network = new Network("127.0.0.16", "255.255.255.252");

        $expected = [
            "127.0.0.17",
            "127.0.0.18",
        ];

        $range = $network->getAllIp();
        $this->assertEquals($expected, $range, 'IP range doesn\'t match.');

        // 127.0.0.16/31
        $network = new Network("127.0.0.16", "255.255.255.254");

        $expected = [];

        $range = $network->getAllIp();
        $this->assertEquals($expected, $range, 'IP range doesn\'t match.');
    }

    public function testGetNextNetwork()
    {
        // 127.0.0.16/28
        $network = new Network("127.0.0.16", "255.255.255.240");

        $expected = "127.0.0.32";
        $next = (string) $network->getNextNetwork()->getIp();

        $this->assertEquals($expected, $next, 'Next network doesn\'t match.');

        // 127.0.0.16/31
        $network = new Network("127.0.0.16", "255.255.255.254");

        $expected = "127.0.0.18";
        $next = (string) $network->getNextNetwork()->getIp();

        $this->assertEquals($expected, $next, 'Next network doesn\'t match.');

        // 127.0.0.16/32
        $network = new Network("127.0.0.16", "255.255.255.255");

        $expected = "127.0.0.17";
        $next = (string) $network->getNextNetwork()->getIp();

        $this->assertEquals($expected, $next, 'Next network doesn\'t match.');
    }

    public function testSplit()
    {
        $network = new Network("10.0.0.0", "255.255.252.0");
        $expected = [
            new Network("10.0.0.0", "255.255.255.0"),
            new Network("10.0.1.0", "255.255.255.0"),
            new Network("10.0.2.0", "255.255.255.0"),
            new Network("10.0.3.0", "255.255.255.0"),
        ];

        $split = $network->split(new IP("255.255.255.0"));
        $this->assertEquals($split, $expected);
    }

    public function testSplitBadNetmaskException()
    {
        $network = new Network("10.0.0.0", "255.0.0.0");

        $this->expectException(BadNetmaskException::class);

        $network->split(new IP("192.168.1.1"));
    }

    public function testSplitNoDiffException()
    {
        $network = new Network("10.0.0.0", "255.0.0.0");

        $this->expectException(BadNetmaskException::class);

        $network->split(new IP("255.0.0.0"));
    }
}
