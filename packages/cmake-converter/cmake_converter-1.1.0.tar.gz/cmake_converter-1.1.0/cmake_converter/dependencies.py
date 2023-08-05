#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2016-2017:
#   Matthieu Estrada, ttamalfor@gmail.com
#
# This file is part of (CMakeConverter).
#
# (CMakeConverter) is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# (CMakeConverter) is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with (CMakeConverter).  If not, see <http://www.gnu.org/licenses/>.

"""
    Dependencies
    ============
     Manage directories and libraries of project dependencies
"""

import ntpath
import os
import re

from cmake_converter.message import send


class Dependencies(object):
    """
        Class who find and write dependencies of project, additionnal directories...
    """

    def __init__(self, data):
        self.cmake = data['cmake']
        self.tree = data['vcxproj']['tree']
        self.ns = data['vcxproj']['ns']
        self.dependencies = data['dependencies']

    def write_include_dir(self):
        """
        Write on "CMakeLists.txt" include directories required for compilation.

        """

        incl_dir = self.tree.find(
            '//ns:ItemGroup/ns:ClCompile/ns:AdditionalIncludeDirectories',
            namespaces=self.ns
        )
        if incl_dir is None:
            incl_dir = self.tree.find(
                '//ns:ItemDefinitionGroup/ns:ClCompile/ns:AdditionalIncludeDirectories',
                namespaces=self.ns
            )

        if incl_dir is not None:
            self.cmake.write('# Include directories \n')
            inc_dir = incl_dir.text.replace('$(ProjectDir)', './')
            for i in inc_dir.split(';'):
                i = i.replace('\\', '/')
                i = re.sub(r'\$\((.+?)\)', r'$ENV{\1}', i)
                self.cmake.write('include_directories(%s)\n' % i)
                send('Include Directories found : %s' % i, 'warn')
            self.cmake.write('\n')
        else:  # pragma: no cover
            send('Include Directories not found for this project.', 'warn')

    def write_dependencies(self):
        """
        Write on "CMakeLists.txt" subdirectories or link directories for external libraries.

        """

        references = self.tree.xpath('//ns:ProjectReference', namespaces=self.ns)
        if references:
            self.cmake.write('################### Dependencies ##################\n'
                             '# Add Dependencies to project.                    #\n'
                             '###################################################\n\n')
            self.cmake.write(
                'option(BUILD_DEPENDS \n' +
                '   "Build other CMake project." \n' +
                '   ON \n' +
                ')\n\n'
            )
            self.cmake.write(
                '# Dependencies : disable BUILD_DEPENDS to link with lib already build.\n'
            )
            if self.dependencies is None:
                self.cmake.write('if(BUILD_DEPENDS)\n')
                for ref in references:
                    reference = str(ref.get('Include'))
                    path_to_reference = os.path.splitext(ntpath.basename(reference))[0]
                    self.cmake.write(
                        '   add_subdirectory(platform/cmake/%s ${CMAKE_BINARY_DIR}/%s)\n' % (
                            path_to_reference, path_to_reference
                        )
                    )
            else:
                self.cmake.write('if(BUILD_DEPENDS)\n')
                d = 1
                for ref in self.dependencies:
                    self.cmake.write(
                        '   add_subdirectory(%s ${CMAKE_BINARY_DIR}/lib%s)\n' % (ref, str(d)))
                    send(
                        'Add manually dependencies : %s. Will be build in "lib%s/" !' % (
                            ref, str(d)),
                        'warn'
                    )
                    d += 1
            self.cmake.write('else()\n')
            for ref in references:
                reference = str(ref.get('Include'))
                path_to_reference = os.path.splitext(ntpath.basename(reference))[0]
                self.cmake.write(
                    '   link_directories(dependencies/%s/build/)\n' % path_to_reference
                )
            self.cmake.write('endif()\n\n')
        else:  # pragma: no cover
            send('No link needed.', '')

    def link_dependencies(self):
        """
        Write link dependencies of project.

        """

        # External libraries
        references = self.tree.xpath('//ns:ProjectReference', namespaces=self.ns)
        if references:
            self.cmake.write('# Link with other dependencies.\n')
            self.cmake.write('target_link_libraries(${PROJECT_NAME} ')
            for ref in references:
                reference = str(ref.get('Include'))
                path_to_reference = os.path.splitext(ntpath.basename(reference))[0]
                lib = os.path.splitext(ntpath.basename(reference))[0]
                if lib == 'g3log':
                    lib += 'ger'  # To get "g3logger"
                self.cmake.write(lib + ' ')
                message = 'External library found : %s' % path_to_reference
                send(message, '')
            self.cmake.write(')\n')

        # Additional Dependencies
        dependencies = self.tree.xpath('//ns:AdditionalDependencies', namespaces=self.ns)
        if dependencies:
            listdepends = dependencies[0].text.replace('%(AdditionalDependencies)', '')
            if listdepends != '':
                send('Additional Dependencies = %s' % listdepends, 'ok')
                windepends = []
                for d in listdepends.split(';'):
                    if d != '%(AdditionalDependencies)':
                        if os.path.splitext(d)[1] == '.lib':
                            windepends.append(d)
                if windepends:
                    self.cmake.write('if(MSVC)\n')
                    self.cmake.write('   target_link_libraries(${PROJECT_NAME} ')
                    for dep in windepends:
                        self.cmake.write(dep + ' ')
                    self.cmake.write(')\n')
                    self.cmake.write('endif(MSVC)\n')
        else:  # pragma: no cover
            send('No dependencies.', '')
