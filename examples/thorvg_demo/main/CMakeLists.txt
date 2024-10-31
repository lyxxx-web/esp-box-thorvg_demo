idf_component_register(
    SRCS "display_main.c"
    INCLUDE_DIRS ".")

idf_component_get_property(TARGET_COMPONENT_PATH espressif__thorvg COMPONENT_DIR)

# set(TARGET_DIR "${CMAKE_BINARY_DIR}/assets")
# set(SOURCE_DIR "${TARGET_COMPONENT_PATH}/thorvg/test/resources")
# file(MAKE_DIRECTORY ${TARGET_DIR})

# add_custom_target(copy_directory ALL
#     COMMAND ${CMAKE_COMMAND} -E copy_directory ${SOURCE_DIR} ${TARGET_DIR}
#     DEPENDS ${SOURCE_DIR}
#     COMMENT "Copying directory ${SOURCE_DIR} to ${TARGET_DIR}"
# )

# add_custom_target(remove_unwanted_files ALL
#     COMMAND ${CMAKE_COMMAND} -E remove -f ${TARGET_DIR}/*.ttf ${TARGET_DIR}/*.raw.png
#     COMMENT "Removing files with '.ttf' or '.raw.png' from ${TARGET_DIR}"
#     DEPENDS copy_directory
# )

# add_dependencies(remove_unwanted_files copy_directory)

spiffs_create_partition_assets(storage ./assets FLASH_IN_PROJECT)
# add_dependencies(spiffs_storage_bin remove_unwanted_files)
