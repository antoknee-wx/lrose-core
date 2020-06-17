/* *=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=* */
/* ** Copyright UCAR                                                         */
/* ** University Corporation for Atmospheric Research (UCAR)                 */
/* ** National Center for Atmospheric Research (NCAR)                        */
/* ** Boulder, Colorado, USA                                                 */
/* ** BSD licence applies - redistribution and use in source and binary      */
/* ** forms, with or without modification, are permitted provided that       */
/* ** the following conditions are met:                                      */
/* ** 1) If the software is modified to produce derivative works,            */
/* ** such modified software should be clearly marked, so as not             */
/* ** to confuse it with the version available from UCAR.                    */
/* ** 2) Redistributions of source code must retain the above copyright      */
/* ** notice, this list of conditions and the following disclaimer.          */
/* ** 3) Redistributions in binary form must reproduce the above copyright   */
/* ** notice, this list of conditions and the following disclaimer in the    */
/* ** documentation and/or other materials provided with the distribution.   */
/* ** 4) Neither the name of UCAR nor the names of its contributors,         */
/* ** if any, may be used to endorse or promote products derived from        */
/* ** this software without specific prior written permission.               */
/* ** DISCLAIMER: THIS SOFTWARE IS PROVIDED 'AS IS' AND WITHOUT ANY EXPRESS  */
/* ** OR IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED      */
/* ** WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.    */
/* *=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=* */
////////////////////////////////////////////
// Params.cc
//
// TDRP C++ code file for class 'Params'.
//
// Code for program hiResNidsVil2Mdv
//
// This file has been automatically
// generated by TDRP, do not modify.
//
/////////////////////////////////////////////

/**
 *
 * @file Params.cc
 *
 * @class Params
 *
 * This class is automatically generated by the Table
 * Driven Runtime Parameters (TDRP) system
 *
 * @note Source is automatically generated from
 *       paramdef file at compile time, do not modify
 *       since modifications will be overwritten.
 *
 *
 * @author Automatically generated
 *
 */
#include "Params.hh"
#include <cstring>

  ////////////////////////////////////////////
  // Default constructor
  //

  Params::Params()

  {

    // zero out table

    memset(_table, 0, sizeof(_table));

    // zero out members

    memset(&_start_, 0, &_end_ - &_start_);

    // class name

    _className = "Params";

    // initialize table

    _init();

    // set members

    tdrpTable2User(_table, &_start_);

    _exitDeferred = false;

  }

  ////////////////////////////////////////////
  // Copy constructor
  //

  Params::Params(const Params& source)

  {

    // sync the source object

    source.sync();

    // zero out table

    memset(_table, 0, sizeof(_table));

    // zero out members

    memset(&_start_, 0, &_end_ - &_start_);

    // class name

    _className = "Params";

    // copy table

    tdrpCopyTable((TDRPtable *) source._table, _table);

    // set members

    tdrpTable2User(_table, &_start_);

    _exitDeferred = false;

  }

  ////////////////////////////////////////////
  // Destructor
  //

  Params::~Params()

  {

    // free up

    freeAll();

  }

  ////////////////////////////////////////////
  // Assignment
  //

  void Params::operator=(const Params& other)

  {

    // sync the other object

    other.sync();

    // free up any existing memory

    freeAll();

    // zero out table

    memset(_table, 0, sizeof(_table));

    // zero out members

    memset(&_start_, 0, &_end_ - &_start_);

    // copy table

    tdrpCopyTable((TDRPtable *) other._table, _table);

    // set members

    tdrpTable2User(_table, &_start_);

    _exitDeferred = other._exitDeferred;

  }

  ////////////////////////////////////////////
  // loadFromArgs()
  //
  // Loads up TDRP using the command line args.
  //
  // Check usage() for command line actions associated with
  // this function.
  //
  //   argc, argv: command line args
  //
  //   char **override_list: A null-terminated list of overrides
  //     to the parameter file.
  //     An override string has exactly the format of an entry
  //     in the parameter file itself.
  //
  //   char **params_path_p:
  //     If this is non-NULL, it is set to point to the path
  //     of the params file used.
  //
  //   bool defer_exit: normally, if the command args contain a 
  //      print or check request, this function will call exit().
  //      If defer_exit is set, such an exit is deferred and the
  //      private member _exitDeferred is set.
  //      Use exidDeferred() to test this flag.
  //
  //  Returns 0 on success, -1 on failure.
  //

  int Params::loadFromArgs(int argc, char **argv,
                           char **override_list,
                           char **params_path_p,
                           bool defer_exit)
  {
    int exit_deferred;
    if (_tdrpLoadFromArgs(argc, argv,
                          _table, &_start_,
                          override_list, params_path_p,
                          _className,
                          defer_exit, &exit_deferred)) {
      return (-1);
    } else {
      if (exit_deferred) {
        _exitDeferred = true;
      }
      return (0);
    }
  }

  ////////////////////////////////////////////
  // loadApplyArgs()
  //
  // Loads up TDRP using the params path passed in, and applies
  // the command line args for printing and checking.
  //
  // Check usage() for command line actions associated with
  // this function.
  //
  //   const char *param_file_path: the parameter file to be read in
  //
  //   argc, argv: command line args
  //
  //   char **override_list: A null-terminated list of overrides
  //     to the parameter file.
  //     An override string has exactly the format of an entry
  //     in the parameter file itself.
  //
  //   bool defer_exit: normally, if the command args contain a 
  //      print or check request, this function will call exit().
  //      If defer_exit is set, such an exit is deferred and the
  //      private member _exitDeferred is set.
  //      Use exidDeferred() to test this flag.
  //
  //  Returns 0 on success, -1 on failure.
  //

  int Params::loadApplyArgs(const char *params_path,
                            int argc, char **argv,
                            char **override_list,
                            bool defer_exit)
  {
    int exit_deferred;
    if (tdrpLoadApplyArgs(params_path, argc, argv,
                          _table, &_start_,
                          override_list,
                          _className,
                          defer_exit, &exit_deferred)) {
      return (-1);
    } else {
      if (exit_deferred) {
        _exitDeferred = true;
      }
      return (0);
    }
  }

  ////////////////////////////////////////////
  // isArgValid()
  // 
  // Check if a command line arg is a valid TDRP arg.
  //

  bool Params::isArgValid(const char *arg)
  {
    return (tdrpIsArgValid(arg));
  }

  ////////////////////////////////////////////
  // isArgValid()
  // 
  // Check if a command line arg is a valid TDRP arg.
  // return number of args consumed.
  //

  int Params::isArgValidN(const char *arg)
  {
    return (tdrpIsArgValidN(arg));
  }

  ////////////////////////////////////////////
  // load()
  //
  // Loads up TDRP for a given class.
  //
  // This version of load gives the programmer the option to load
  // up more than one class for a single application. It is a
  // lower-level routine than loadFromArgs, and hence more
  // flexible, but the programmer must do more work.
  //
  //   const char *param_file_path: the parameter file to be read in.
  //
  //   char **override_list: A null-terminated list of overrides
  //     to the parameter file.
  //     An override string has exactly the format of an entry
  //     in the parameter file itself.
  //
  //   expand_env: flag to control environment variable
  //               expansion during tokenization.
  //               If TRUE, environment expansion is set on.
  //               If FALSE, environment expansion is set off.
  //
  //  Returns 0 on success, -1 on failure.
  //

  int Params::load(const char *param_file_path,
                   char **override_list,
                   int expand_env, int debug)
  {
    if (tdrpLoad(param_file_path,
                 _table, &_start_,
                 override_list,
                 expand_env, debug)) {
      return (-1);
    } else {
      return (0);
    }
  }

  ////////////////////////////////////////////
  // loadFromBuf()
  //
  // Loads up TDRP for a given class.
  //
  // This version of load gives the programmer the option to
  // load up more than one module for a single application,
  // using buffers which have been read from a specified source.
  //
  //   const char *param_source_str: a string which describes the
  //     source of the parameter information. It is used for
  //     error reporting only.
  //
  //   char **override_list: A null-terminated list of overrides
  //     to the parameter file.
  //     An override string has exactly the format of an entry
  //     in the parameter file itself.
  //
  //   const char *inbuf: the input buffer
  //
  //   int inlen: length of the input buffer
  //
  //   int start_line_num: the line number in the source which
  //     corresponds to the start of the buffer.
  //
  //   expand_env: flag to control environment variable
  //               expansion during tokenization.
  //               If TRUE, environment expansion is set on.
  //               If FALSE, environment expansion is set off.
  //
  //  Returns 0 on success, -1 on failure.
  //

  int Params::loadFromBuf(const char *param_source_str,
                          char **override_list,
                          const char *inbuf, int inlen,
                          int start_line_num,
                          int expand_env, int debug)
  {
    if (tdrpLoadFromBuf(param_source_str,
                        _table, &_start_,
                        override_list,
                        inbuf, inlen, start_line_num,
                        expand_env, debug)) {
      return (-1);
    } else {
      return (0);
    }
  }

  ////////////////////////////////////////////
  // loadDefaults()
  //
  // Loads up default params for a given class.
  //
  // See load() for more detailed info.
  //
  //  Returns 0 on success, -1 on failure.
  //

  int Params::loadDefaults(int expand_env)
  {
    if (tdrpLoad(NULL,
                 _table, &_start_,
                 NULL, expand_env, FALSE)) {
      return (-1);
    } else {
      return (0);
    }
  }

  ////////////////////////////////////////////
  // sync()
  //
  // Syncs the user struct data back into the parameter table,
  // in preparation for printing.
  //
  // This function alters the table in a consistent manner.
  // Therefore it can be regarded as const.
  //

  void Params::sync(void) const
  {
    tdrpUser2Table(_table, (char *) &_start_);
  }

  ////////////////////////////////////////////
  // print()
  // 
  // Print params file
  //
  // The modes supported are:
  //
  //   PRINT_SHORT:   main comments only, no help or descriptions
  //                  structs and arrays on a single line
  //   PRINT_NORM:    short + descriptions and help
  //   PRINT_LONG:    norm  + arrays and structs expanded
  //   PRINT_VERBOSE: long  + private params included
  //

  void Params::print(FILE *out, tdrp_print_mode_t mode)
  {
    tdrpPrint(out, _table, _className, mode);
  }

  ////////////////////////////////////////////
  // checkAllSet()
  //
  // Return TRUE if all set, FALSE if not.
  //
  // If out is non-NULL, prints out warning messages for those
  // parameters which are not set.
  //

  int Params::checkAllSet(FILE *out)
  {
    return (tdrpCheckAllSet(out, _table, &_start_));
  }

  //////////////////////////////////////////////////////////////
  // checkIsSet()
  //
  // Return TRUE if parameter is set, FALSE if not.
  //
  //

  int Params::checkIsSet(const char *paramName)
  {
    return (tdrpCheckIsSet(paramName, _table, &_start_));
  }

  ////////////////////////////////////////////
  // freeAll()
  //
  // Frees up all TDRP dynamic memory.
  //

  void Params::freeAll(void)
  {
    tdrpFreeAll(_table, &_start_);
  }

  ////////////////////////////////////////////
  // usage()
  //
  // Prints out usage message for TDRP args as passed
  // in to loadFromArgs().
  //

  void Params::usage(ostream &out)
  {
    out << "TDRP args: [options as below]\n"
        << "   [ -params/--params path ] specify params file path\n"
        << "   [ -check_params/--check_params] check which params are not set\n"
        << "   [ -print_params/--print_params [mode]] print parameters\n"
        << "     using following modes, default mode is 'norm'\n"
        << "       short:   main comments only, no help or descr\n"
        << "                structs and arrays on a single line\n"
        << "       norm:    short + descriptions and help\n"
        << "       long:    norm  + arrays and structs expanded\n"
        << "       verbose: long  + private params included\n"
        << "       short_expand:   short with env vars expanded\n"
        << "       norm_expand:    norm with env vars expanded\n"
        << "       long_expand:    long with env vars expanded\n"
        << "       verbose_expand: verbose with env vars expanded\n"
        << "   [ -tdrp_debug] debugging prints for tdrp\n"
        << "   [ -tdrp_usage] print this usage\n";
  }

  ////////////////////////////////////////////
  // arrayRealloc()
  //
  // Realloc 1D array.
  //
  // If size is increased, the values from the last array 
  // entry is copied into the new space.
  //
  // Returns 0 on success, -1 on error.
  //

  int Params::arrayRealloc(const char *param_name, int new_array_n)
  {
    if (tdrpArrayRealloc(_table, &_start_,
                         param_name, new_array_n)) {
      return (-1);
    } else {
      return (0);
    }
  }

  ////////////////////////////////////////////
  // array2DRealloc()
  //
  // Realloc 2D array.
  //
  // If size is increased, the values from the last array 
  // entry is copied into the new space.
  //
  // Returns 0 on success, -1 on error.
  //

  int Params::array2DRealloc(const char *param_name,
                             int new_array_n1,
                             int new_array_n2)
  {
    if (tdrpArray2DRealloc(_table, &_start_, param_name,
                           new_array_n1, new_array_n2)) {
      return (-1);
    } else {
      return (0);
    }
  }

  ////////////////////////////////////////////
  // _init()
  //
  // Class table initialization function.
  //
  //

  void Params::_init()

  {

    TDRPtable *tt = _table;

    // Parameter 'Comment 0'
    
    memset(tt, 0, sizeof(TDRPtable));
    tt->ptype = COMMENT_TYPE;
    tt->param_name = tdrpStrDup("Comment 0");
    tt->comment_hdr = tdrpStrDup("hiResNidsVil2Mdv reads the high resolution NIDS\nVIL level three radial data files, remaps them to\ncartesian ordinates and writes the data out as mdv.\nThis format started in late 2010. Niles Oien.");
    tt->comment_text = tdrpStrDup("");
    tt++;
    
    // Parameter 'radars'
    // ctype is 'char*'
    
    memset(tt, 0, sizeof(TDRPtable));
    tt->ptype = STRING_TYPE;
    tt->param_name = tdrpStrDup("radars");
    tt->descr = tdrpStrDup("List of radars to process.");
    tt->help = tdrpStrDup("Used to construe input file directories and output URLs. Note\nthat if an environment variable is used that is not set as a radar name,\nthen that entry is skipped.");
    tt->array_offset = (char *) &_radars - &_start_;
    tt->array_n_offset = (char *) &radars_n - &_start_;
    tt->is_array = TRUE;
    tt->array_len_fixed = FALSE;
    tt->array_elem_size = sizeof(char*);
    tt->array_n = 10;
    tt->array_vals = (tdrpVal_t *)
        tdrpMalloc(tt->array_n * sizeof(tdrpVal_t));
      tt->array_vals[0].s = tdrpStrDup("$(RADAR1)");
      tt->array_vals[1].s = tdrpStrDup("$(RADAR2)");
      tt->array_vals[2].s = tdrpStrDup("$(RADAR3)");
      tt->array_vals[3].s = tdrpStrDup("$(RADAR4)");
      tt->array_vals[4].s = tdrpStrDup("$(RADAR5)");
      tt->array_vals[5].s = tdrpStrDup("$(RADAR6)");
      tt->array_vals[6].s = tdrpStrDup("$(RADAR7)");
      tt->array_vals[7].s = tdrpStrDup("$(RADAR8)");
      tt->array_vals[8].s = tdrpStrDup("$(RADAR9)");
      tt->array_vals[9].s = tdrpStrDup("$(RADAR10)");
    tt++;
    
    // Parameter 'field'
    // ctype is '_field_t'
    
    memset(tt, 0, sizeof(TDRPtable));
    tt->ptype = STRUCT_TYPE;
    tt->param_name = tdrpStrDup("field");
    tt->descr = tdrpStrDup("List of fields to process for each radar, and optionto save as radial (preferred).");
    tt->help = tdrpStrDup("Set as appropriate");
    tt->val_offset = (char *) &field - &_start_;
    tt->struct_def.name = tdrpStrDup("field_t");
    tt->struct_def.nfields = 3;
    tt->struct_def.fields = (struct_field_t *)
        tdrpMalloc(tt->struct_def.nfields * sizeof(struct_field_t));
      tt->struct_def.fields[0].ftype = tdrpStrDup("string");
      tt->struct_def.fields[0].fname = tdrpStrDup("inFieldName");
      tt->struct_def.fields[0].ptype = STRING_TYPE;
      tt->struct_def.fields[0].rel_offset = 
        (char *) &field.inFieldName - (char *) &field;
      tt->struct_def.fields[1].ftype = tdrpStrDup("string");
      tt->struct_def.fields[1].fname = tdrpStrDup("outDirName");
      tt->struct_def.fields[1].ptype = STRING_TYPE;
      tt->struct_def.fields[1].rel_offset = 
        (char *) &field.outDirName - (char *) &field;
      tt->struct_def.fields[2].ftype = tdrpStrDup("boolean");
      tt->struct_def.fields[2].fname = tdrpStrDup("saveAsRadial");
      tt->struct_def.fields[2].ptype = BOOL_TYPE;
      tt->struct_def.fields[2].rel_offset = 
        (char *) &field.saveAsRadial - (char *) &field;
    tt->n_struct_vals = 3;
    tt->struct_vals = (tdrpVal_t *)
        tdrpMalloc(tt->n_struct_vals * sizeof(tdrpVal_t));
      tt->struct_vals[0].s = tdrpStrDup("DVL");
      tt->struct_vals[1].s = tdrpStrDup("vil");
      tt->struct_vals[2].b = pTRUE;
    tt++;
    
    // Parameter 'topInDir'
    // ctype is 'char*'
    
    memset(tt, 0, sizeof(TDRPtable));
    tt->ptype = STRING_TYPE;
    tt->param_name = tdrpStrDup("topInDir");
    tt->descr = tdrpStrDup("Top input directory.");
    tt->help = tdrpStrDup("Files are named by convention :\n{topInDir}/{radar}/{inField}/{date}/{date}.{time}.{inField}\nfor instance\n/raid/ext_obs/ldm/nids/uc/nids/LWX/BREF1/20101104/20101104.1611.BREF1\nwould be a typical name.");
    tt->val_offset = (char *) &topInDir - &_start_;
    tt->single_val.s = tdrpStrDup("/raid/ext_obs/ldm/nids/uc/nids");
    tt++;
    
    // Parameter 'topOutUrl'
    // ctype is 'char*'
    
    memset(tt, 0, sizeof(TDRPtable));
    tt->ptype = STRING_TYPE;
    tt->param_name = tdrpStrDup("topOutUrl");
    tt->descr = tdrpStrDup("Top output URL for mdv data.");
    tt->help = tdrpStrDup("This has the output field name and the radar\nname appened to it, so mdvp:://localhost::$(PROJECT)/mdv\nfor field dbz1 and radar LWX will become\nmdvp:://localhost::$(PROJECT)/mdv/dbz1/LWX");
    tt->val_offset = (char *) &topOutUrl - &_start_;
    tt->single_val.s = tdrpStrDup("mdvp:://localhost::$(PROJECT)/mdv");
    tt++;
    
    // Parameter 'Comment 1'
    
    memset(tt, 0, sizeof(TDRPtable));
    tt->ptype = COMMENT_TYPE;
    tt->param_name = tdrpStrDup("Comment 1");
    tt->comment_hdr = tdrpStrDup("DEBUGGING AND PROCESS CONTROL");
    tt->comment_text = tdrpStrDup("");
    tt++;
    
    // Parameter 'debug'
    // ctype is 'tdrp_bool_t'
    
    memset(tt, 0, sizeof(TDRPtable));
    tt->ptype = BOOL_TYPE;
    tt->param_name = tdrpStrDup("debug");
    tt->descr = tdrpStrDup("Debug option");
    tt->help = tdrpStrDup("If set, debug messages will be printed appropriately");
    tt->val_offset = (char *) &debug - &_start_;
    tt->single_val.b = pFALSE;
    tt++;
    
    // Parameter 'lightweightFileSearch'
    // ctype is 'tdrp_bool_t'
    
    memset(tt, 0, sizeof(TDRPtable));
    tt->ptype = BOOL_TYPE;
    tt->param_name = tdrpStrDup("lightweightFileSearch");
    tt->descr = tdrpStrDup("Option to use a lightweight file search in realtime.");
    tt->help = tdrpStrDup("This helps with load issues. If FALSE then a\nDsInputPath search is done which may be harder on the filesystem.\nLightweight assumes that YYYYMMDD directory names are used.");
    tt->val_offset = (char *) &lightweightFileSearch - &_start_;
    tt->single_val.b = pFALSE;
    tt++;
    
    // Parameter 'debugRealtimeFileSearch'
    // ctype is 'tdrp_bool_t'
    
    memset(tt, 0, sizeof(TDRPtable));
    tt->ptype = BOOL_TYPE;
    tt->param_name = tdrpStrDup("debugRealtimeFileSearch");
    tt->descr = tdrpStrDup("Option to debug looking for new files in realtime mode only.");
    tt->help = tdrpStrDup("Generally should not have to do this.");
    tt->val_offset = (char *) &debugRealtimeFileSearch - &_start_;
    tt->single_val.b = pFALSE;
    tt++;
    
    // Parameter 'dirScanSleep'
    // ctype is 'int'
    
    memset(tt, 0, sizeof(TDRPtable));
    tt->ptype = INT_TYPE;
    tt->param_name = tdrpStrDup("dirScanSleep");
    tt->descr = tdrpStrDup("Number of seconds to wait between searches for new files.");
    tt->help = tdrpStrDup("Range will be truncated from 5 to 50 internally.\nSetting this too low can cause the load to be very high as\na large number of directories may be used for input, and there are\nno _latest_data_info files.");
    tt->val_offset = (char *) &dirScanSleep - &_start_;
    tt->single_val.i = 30;
    tt++;
    
    // Parameter 'instance'
    // ctype is 'char*'
    
    memset(tt, 0, sizeof(TDRPtable));
    tt->ptype = STRING_TYPE;
    tt->param_name = tdrpStrDup("instance");
    tt->descr = tdrpStrDup("Process instance");
    tt->help = tdrpStrDup("Used for registration with procmap.");
    tt->val_offset = (char *) &instance - &_start_;
    tt->single_val.s = tdrpStrDup("primary");
    tt++;
    
    // Parameter 'mode'
    // ctype is '_op_mode'
    
    memset(tt, 0, sizeof(TDRPtable));
    tt->ptype = ENUM_TYPE;
    tt->param_name = tdrpStrDup("mode");
    tt->descr = tdrpStrDup("Operation mode");
    tt->help = tdrpStrDup("Program may be run in two modes, archive and realtime.\nIn realtime mode files are converted as they come in, in\narchive mode all files in the tree are converted.");
    tt->val_offset = (char *) &mode - &_start_;
    tt->enum_def.name = tdrpStrDup("op_mode");
    tt->enum_def.nfields = 2;
    tt->enum_def.fields = (enum_field_t *)
        tdrpMalloc(tt->enum_def.nfields * sizeof(enum_field_t));
      tt->enum_def.fields[0].name = tdrpStrDup("ARCHIVE");
      tt->enum_def.fields[0].val = ARCHIVE;
      tt->enum_def.fields[1].name = tdrpStrDup("REALTIME");
      tt->enum_def.fields[1].val = REALTIME;
    tt->single_val.e = REALTIME;
    tt++;
    
    // Parameter 'max_realtime_valid_age'
    // ctype is 'int'
    
    memset(tt, 0, sizeof(TDRPtable));
    tt->ptype = INT_TYPE;
    tt->param_name = tdrpStrDup("max_realtime_valid_age");
    tt->descr = tdrpStrDup("Max age of input data files, seconds");
    tt->help = tdrpStrDup("For realtime only. Keep this *very* short or the load\nwill spike like crazy on startup in realtime mode - or set\nstaggerProcs to TRUE.");
    tt->val_offset = (char *) &max_realtime_valid_age - &_start_;
    tt->single_val.i = 60;
    tt++;
    
    // Parameter 'stagger'
    // ctype is '_stagger_t'
    
    memset(tt, 0, sizeof(TDRPtable));
    tt->ptype = STRUCT_TYPE;
    tt->param_name = tdrpStrDup("stagger");
    tt->descr = tdrpStrDup("Option to stagger startup of child processes\nin realtime mode.");
    tt->help = tdrpStrDup("If staggerProcs s TRUE, child processes are\ninitially delayed so that they only start at intervals\nof procStaggerSecs seconds to avoid them all starting\nat once. The default of 15 second should be fine. Only\nhas an effect on startup, the intent is to avoid\na load spike for startup in realtime mode.\n\nThe other option is to keep max_realtime_valid_age\nsmall, like 60 seconds.");
    tt->val_offset = (char *) &stagger - &_start_;
    tt->struct_def.name = tdrpStrDup("stagger_t");
    tt->struct_def.nfields = 2;
    tt->struct_def.fields = (struct_field_t *)
        tdrpMalloc(tt->struct_def.nfields * sizeof(struct_field_t));
      tt->struct_def.fields[0].ftype = tdrpStrDup("boolean");
      tt->struct_def.fields[0].fname = tdrpStrDup("staggerProcs");
      tt->struct_def.fields[0].ptype = BOOL_TYPE;
      tt->struct_def.fields[0].rel_offset = 
        (char *) &stagger.staggerProcs - (char *) &stagger;
      tt->struct_def.fields[1].ftype = tdrpStrDup("int");
      tt->struct_def.fields[1].fname = tdrpStrDup("procStaggerSecs");
      tt->struct_def.fields[1].ptype = INT_TYPE;
      tt->struct_def.fields[1].rel_offset = 
        (char *) &stagger.procStaggerSecs - (char *) &stagger;
    tt->n_struct_vals = 2;
    tt->struct_vals = (tdrpVal_t *)
        tdrpMalloc(tt->n_struct_vals * sizeof(tdrpVal_t));
      tt->struct_vals[0].b = pFALSE;
      tt->struct_vals[1].i = 15;
    tt++;
    
    // Parameter 'expiry'
    // ctype is 'long'
    
    memset(tt, 0, sizeof(TDRPtable));
    tt->ptype = LONG_TYPE;
    tt->param_name = tdrpStrDup("expiry");
    tt->descr = tdrpStrDup("How long the data are valid, seconds.");
    tt->help = tdrpStrDup("Depends on input frequency.");
    tt->val_offset = (char *) &expiry - &_start_;
    tt->single_val.l = 600;
    tt++;
    
    // Parameter 'res'
    // ctype is '_res_t'
    
    memset(tt, 0, sizeof(TDRPtable));
    tt->ptype = STRUCT_TYPE;
    tt->param_name = tdrpStrDup("res");
    tt->descr = tdrpStrDup("Cartesian resolution and overage, Km.");
    tt->help = tdrpStrDup("Delta is the resoltion to remap to.\ndist is the max range to be covered from the radar to the end\nof the data.\n\nIf delta in negative, the polar resolution is used.\nIf dist is negative, the maximum range for the data is used.");
    tt->val_offset = (char *) &res - &_start_;
    tt->struct_def.name = tdrpStrDup("res_t");
    tt->struct_def.nfields = 2;
    tt->struct_def.fields = (struct_field_t *)
        tdrpMalloc(tt->struct_def.nfields * sizeof(struct_field_t));
      tt->struct_def.fields[0].ftype = tdrpStrDup("double");
      tt->struct_def.fields[0].fname = tdrpStrDup("delta");
      tt->struct_def.fields[0].ptype = DOUBLE_TYPE;
      tt->struct_def.fields[0].rel_offset = 
        (char *) &res.delta - (char *) &res;
      tt->struct_def.fields[1].ftype = tdrpStrDup("double");
      tt->struct_def.fields[1].fname = tdrpStrDup("dist");
      tt->struct_def.fields[1].ptype = DOUBLE_TYPE;
      tt->struct_def.fields[1].rel_offset = 
        (char *) &res.dist - (char *) &res;
    tt->n_struct_vals = 2;
    tt->struct_vals = (tdrpVal_t *)
        tdrpMalloc(tt->n_struct_vals * sizeof(tdrpVal_t));
      tt->struct_vals[0].d = 0.25;
      tt->struct_vals[1].d = -1;
    tt++;
    
    // Parameter 'byteSwap'
    // ctype is 'tdrp_bool_t'
    
    memset(tt, 0, sizeof(TDRPtable));
    tt->ptype = BOOL_TYPE;
    tt->param_name = tdrpStrDup("byteSwap");
    tt->descr = tdrpStrDup("Option to swap bytes.");
    tt->help = tdrpStrDup("On a PC, set to TRUE.");
    tt->val_offset = (char *) &byteSwap - &_start_;
    tt->single_val.b = pTRUE;
    tt++;
    
    // Parameter 'forkIt'
    // ctype is 'tdrp_bool_t'
    
    memset(tt, 0, sizeof(TDRPtable));
    tt->ptype = BOOL_TYPE;
    tt->param_name = tdrpStrDup("forkIt");
    tt->descr = tdrpStrDup("Option to fork processes.");
    tt->help = tdrpStrDup("If FALSE, threads are used instead.");
    tt->val_offset = (char *) &forkIt - &_start_;
    tt->single_val.b = pTRUE;
    tt++;
    
    // Parameter 'threadLimit'
    // ctype is '_threadLimit_t'
    
    memset(tt, 0, sizeof(TDRPtable));
    tt->ptype = STRUCT_TYPE;
    tt->param_name = tdrpStrDup("threadLimit");
    tt->descr = tdrpStrDup("If threads are used (forkIt is FALSE) then only\nallow maxNumThreads to be actively processing a file at once.");
    tt->help = tdrpStrDup("Useful to avoid load issues.");
    tt->val_offset = (char *) &threadLimit - &_start_;
    tt->struct_def.name = tdrpStrDup("threadLimit_t");
    tt->struct_def.nfields = 2;
    tt->struct_def.fields = (struct_field_t *)
        tdrpMalloc(tt->struct_def.nfields * sizeof(struct_field_t));
      tt->struct_def.fields[0].ftype = tdrpStrDup("boolean");
      tt->struct_def.fields[0].fname = tdrpStrDup("limitNumThreads");
      tt->struct_def.fields[0].ptype = BOOL_TYPE;
      tt->struct_def.fields[0].rel_offset = 
        (char *) &threadLimit.limitNumThreads - (char *) &threadLimit;
      tt->struct_def.fields[1].ftype = tdrpStrDup("int");
      tt->struct_def.fields[1].fname = tdrpStrDup("maxNumThreads");
      tt->struct_def.fields[1].ptype = INT_TYPE;
      tt->struct_def.fields[1].rel_offset = 
        (char *) &threadLimit.maxNumThreads - (char *) &threadLimit;
    tt->n_struct_vals = 2;
    tt->struct_vals = (tdrpVal_t *)
        tdrpMalloc(tt->n_struct_vals * sizeof(tdrpVal_t));
      tt->struct_vals[0].b = pTRUE;
      tt->struct_vals[1].i = 3;
    tt++;
    
    // trailing entry has param_name set to NULL
    
    tt->param_name = NULL;
    
    return;
  
  }
