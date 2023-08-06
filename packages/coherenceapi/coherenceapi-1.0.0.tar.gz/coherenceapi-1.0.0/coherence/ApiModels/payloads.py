# Copyright 2018, Bryan Thornbury
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


class CreateApplicationPayload(object):
    def __init__(self, applicationExecutionContext, dockerBaseImage=None):
        '''
        :type applicationExecutionContext: ApplicationExecutionContext
        :type dockerBaseImage: str
        '''
        self.applicationExecutionContext = applicationExecutionContext
        self.dockerBaseImage = dockerBaseImage


class CreateJobPayload(object):
    def __init__(self, taskInfo, applicationId, jobType, ramMb=None, scheduledJobCrontab=None):
        self.scheduledJobCrontab = scheduledJobCrontab
        self.jobType = jobType
        self.ramMb = ramMb
        self.applicationId = applicationId
        self.serializedJobEntrypoint = taskInfo.serializeForInjector()


class UploadFilePayload(object):
    def __init__(self, applicationContextFile=None, fileContents=None, applicationId=None):
        self.applicationContextFile = applicationContextFile
        self.applicationGuid = applicationId
        self.fileContents = fileContents

