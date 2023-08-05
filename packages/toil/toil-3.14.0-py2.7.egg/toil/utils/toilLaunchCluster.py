# Copyright (C) 2015 UCSC Computational Genomics Lab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Launches a toil leader instance with the specified provisioner
"""
import logging
from toil.lib.bioio import parseBasicOptions, getBasicOptionParser
from toil.utils import addBasicProvisionerOptions

logger = logging.getLogger(__name__)


def createTagsDict(tagList):
    tagsDict = dict()
    for tag in tagList:
        key, value = tag.split('=')
        tagsDict[key] = value
    return tagsDict


def main():
    parser = getBasicOptionParser()
    parser = addBasicProvisionerOptions(parser)
    parser.add_argument("--leaderNodeType", dest="leaderNodeType", required=True,
                        help="Non-preemptable node type to use for the cluster leader.")
    parser.add_argument("--keyPairName", dest='keyPairName', required=True,
                        help="The name of the AWS key pair to include on the instance")
    parser.add_argument("-t", "--tag", metavar='NAME=VALUE', dest='tags', default=[], action='append',
                        help="Tags are added to the AWS cluster for this node and all of its "
                             "children. Tags are of the form:\n"
                             " --t key1=value1 --tag key2=value2\n"
                             "Multiple tags are allowed and each tag needs its own flag. By "
                             "default the cluster is tagged with "
                             " {\n"
                             "      \"Name\": clusterName,\n"
                             "      \"Owner\": IAM username\n"
                             " }. ")
    parser.add_argument("--vpcSubnet",
                        help="VPC subnet ID to launch cluster in. Uses default subnet if not specified. "
                        "This subnet needs to have auto assign IPs turned on.")
    parser.add_argument("--nodeTypes", dest='nodeTypes', default=None, type=str,
                        help="Comma-separated list of node types to create while launching the leader. The "
                             "syntax for each node type depends on the "
                             "provisioner used. For the aws provisioner this is the name of an "
                             "EC2 instance type followed by a colon and the price in dollar to "
                             "bid for a spot instance, for example 'c3.8xlarge:0.42'. Must also provide "
                             "the --workers argument to specify how many workers of each node type to create")
    parser.add_argument("-w", "--workers", dest='workers', default=None, type=str,
                        help="Comma-separated list of the number of workers of each node type to launch "
                             "alongside the leader when the "
                             "cluster is created. This can be useful if running toil without "
                             "auto-scaling but with need of more hardware support")
    parser.add_argument("--leaderStorage", dest='leaderStorage', type=int, default=50,
                        help="Specify the size (in gigabytes) of the root volume for the leader instance. "
                             "This is an EBS volume.")
    parser.add_argument("--nodeStorage", dest='nodeStorage', type=int, default=50,
                        help="Specify the size (in gigabytes) of the root volume for any worker instances "
                             "created when using the -w flag. This is an EBS volume.")
    config = parseBasicOptions(parser)
    tagsDict = None if config.tags is None else createTagsDict(config.tags)

    spotBids = []
    nodeTypes = []
    preemptableNodeTypes = []
    numNodes = []
    numPreemptableNodes = []
    leaderSpotBid = None
    if config.provisioner == 'aws':
        logger.info('Using aws provisioner.')
        try:
            from toil.provisioners.aws.awsProvisioner import AWSProvisioner
        except ImportError:
            raise RuntimeError('The aws extra must be installed to use this provisioner')
        provisioner = AWSProvisioner()

        #Parse leader node type and spot bid
        parsedBid = config.leaderNodeType.split(':', 1)
        if len(config.leaderNodeType) != len(parsedBid[0]):
            leaderSpotBid = float(parsedBid[1])
            config.leaderNodeType = parsedBid[0]

        if (config.nodeTypes or config.workers) and not (config.nodeTypes and config.workers):
            raise RuntimeError("The --nodeTypes and --workers options must be specified together,")
        if config.nodeTypes:
            nodeTypesList = config.nodeTypes.split(",")
            numWorkersList = config.workers.split(",")
            if not len(nodeTypesList) == len(numWorkersList):
                raise RuntimeError("List of node types must be same length as list of numbers of workers.")
            for nodeTypeStr, num in zip(nodeTypesList, numWorkersList):
                parsedBid = nodeTypeStr.split(':', 1)
                if len(nodeTypeStr) != len(parsedBid[0]):
                    #Is a preemptable node

                    preemptableNodeTypes.append(parsedBid[0])
                    spotBids.append(float(parsedBid[1]))
                    numPreemptableNodes.append(int(num))
                else:
                    nodeTypes.append(nodeTypeStr)
                    numNodes.append(int(num))
    else:
        assert False

    provisioner.launchCluster(leaderNodeType=config.leaderNodeType,
                              leaderSpotBid=leaderSpotBid,
                              nodeTypes=nodeTypes,
                              preemptableNodeTypes=preemptableNodeTypes,
                              numWorkers=numNodes,
                              numPreemptableWorkers = numPreemptableNodes,
                              keyName=config.keyPairName,
                              clusterName=config.clusterName,
                              spotBids=spotBids,
                              userTags=tagsDict,
                              zone=config.zone,
                              leaderStorage=config.leaderStorage,
                              nodeStorage=config.nodeStorage,
                              vpcSubnet=config.vpcSubnet)
