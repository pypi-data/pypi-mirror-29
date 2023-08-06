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


from typing import List


class CreateApplicationResponse(object):
    error = None  # type: bool

    errorMessage = None  # type: str

    applicationId = None  # type: str

    fileHashesRequiringUpload = None  # type: List[str]


class CreateJobResponse(object):
    error = None  # type: bool

    errorMessage = None  # type: str

    jobId = None  # type: str


class JobStatusResponse(object):
    jobId = None  # type: str

    jobStatus = None  # type: str

    returnValueJson = None  # type: str


class ApplicationStatusResponse(object):
    applicationId = None  # type: str

    status = None  # type: str
