# -*- coding: utf-8 -*-
#
# Copyright 2017 Gehirn Inc.
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


class AbstractBaseEndpoint:
    __slots__ = ['repository', 'validator', '_handlers']

    def __init__(self, repository, validator):
        self.repository = repository
        self.validator = validator
        self._handlers = {}

    def _get_handler(self, handler_type):
        return self._handlers[handler_type]

    def register_handler(self, handler, handler_types):
        for handler_type in handler_types:
            self._handlers[handler_type] = handler

    def validate_request(self, request):
        raise NotImplementedError('subclasses must implement this')

    def handle_request(self, request, *args, **kwargs):
        raise NotImplementedError('subclasses must implement this')
