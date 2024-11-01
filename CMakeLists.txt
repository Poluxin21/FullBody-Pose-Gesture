cmake_minimum_required(VERSION 3.10)
project(3D_RENDER_BODYTOVRCHAT)

set(OPENVR_SDK_PATH "${CMAKE_CURRENT_SOURCE_DIR}/src/vrDriver/openvr-2.5.1")

find_package(OpenVR REQUIRED
  HINTS ${OPENVR_SDK_PATH}
  PATHS
    ${OPENVR_SDK_PATH}
)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src)
include_directories(${OpenVR_INCLUDE_DIRS})

add_executable(${PROJECT_NAME} src/main.cpp)

target_link_libraries(${PROJECT_NAME} ${OpenVR_LIBRARIES})

if(MSVC)
  target_compile_options(${PROJECT_NAME} PRIVATE /MT /EHsc)
endif()