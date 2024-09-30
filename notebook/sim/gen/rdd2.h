/* This file was automatically generated by CasADi 3.6.6.
 *  It consists of: 
 *   1) content generated by CasADi runtime: not copyrighted
 *   2) template code copied from CasADi source: permissively licensed (MIT-0)
 *   3) user code: owned by the user
 *
 */
#ifdef __cplusplus
extern "C" {
#endif

#ifndef casadi_real
#define casadi_real double
#endif

#ifndef casadi_int
#define casadi_int long long int
#endif

int attitude_rate_control(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem);
int attitude_rate_control_alloc_mem(void);
int attitude_rate_control_init_mem(int mem);
void attitude_rate_control_free_mem(int mem);
int attitude_rate_control_checkout(void);
void attitude_rate_control_release(int mem);
void attitude_rate_control_incref(void);
void attitude_rate_control_decref(void);
casadi_int attitude_rate_control_n_in(void);
casadi_int attitude_rate_control_n_out(void);
casadi_real attitude_rate_control_default_in(casadi_int i);
const char* attitude_rate_control_name_in(casadi_int i);
const char* attitude_rate_control_name_out(casadi_int i);
const casadi_int* attitude_rate_control_sparsity_in(casadi_int i);
const casadi_int* attitude_rate_control_sparsity_out(casadi_int i);
int attitude_rate_control_work(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w);
int attitude_rate_control_work_bytes(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w);
#define attitude_rate_control_SZ_ARG 11
#define attitude_rate_control_SZ_RES 5
#define attitude_rate_control_SZ_IW 0
#define attitude_rate_control_SZ_W 17
int attitude_control(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem);
int attitude_control_alloc_mem(void);
int attitude_control_init_mem(int mem);
void attitude_control_free_mem(int mem);
int attitude_control_checkout(void);
void attitude_control_release(int mem);
void attitude_control_incref(void);
void attitude_control_decref(void);
casadi_int attitude_control_n_in(void);
casadi_int attitude_control_n_out(void);
casadi_real attitude_control_default_in(casadi_int i);
const char* attitude_control_name_in(casadi_int i);
const char* attitude_control_name_out(casadi_int i);
const casadi_int* attitude_control_sparsity_in(casadi_int i);
const casadi_int* attitude_control_sparsity_out(casadi_int i);
int attitude_control_work(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w);
int attitude_control_work_bytes(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w);
#define attitude_control_SZ_ARG 3
#define attitude_control_SZ_RES 1
#define attitude_control_SZ_IW 0
#define attitude_control_SZ_W 15
int position_control(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem);
int position_control_alloc_mem(void);
int position_control_init_mem(int mem);
void position_control_free_mem(int mem);
int position_control_checkout(void);
void position_control_release(int mem);
void position_control_incref(void);
void position_control_decref(void);
casadi_int position_control_n_in(void);
casadi_int position_control_n_out(void);
casadi_real position_control_default_in(casadi_int i);
const char* position_control_name_in(casadi_int i);
const char* position_control_name_out(casadi_int i);
const casadi_int* position_control_sparsity_in(casadi_int i);
const casadi_int* position_control_sparsity_out(casadi_int i);
int position_control_work(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w);
int position_control_work_bytes(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w);
#define position_control_SZ_ARG 10
#define position_control_SZ_RES 3
#define position_control_SZ_IW 0
#define position_control_SZ_W 30
int joy_acro(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem);
int joy_acro_alloc_mem(void);
int joy_acro_init_mem(int mem);
void joy_acro_free_mem(int mem);
int joy_acro_checkout(void);
void joy_acro_release(int mem);
void joy_acro_incref(void);
void joy_acro_decref(void);
casadi_int joy_acro_n_in(void);
casadi_int joy_acro_n_out(void);
casadi_real joy_acro_default_in(casadi_int i);
const char* joy_acro_name_in(casadi_int i);
const char* joy_acro_name_out(casadi_int i);
const casadi_int* joy_acro_sparsity_in(casadi_int i);
const casadi_int* joy_acro_sparsity_out(casadi_int i);
int joy_acro_work(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w);
int joy_acro_work_bytes(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w);
#define joy_acro_SZ_ARG 6
#define joy_acro_SZ_RES 2
#define joy_acro_SZ_IW 0
#define joy_acro_SZ_W 2
int joy_auto_level(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem);
int joy_auto_level_alloc_mem(void);
int joy_auto_level_init_mem(int mem);
void joy_auto_level_free_mem(int mem);
int joy_auto_level_checkout(void);
void joy_auto_level_release(int mem);
void joy_auto_level_incref(void);
void joy_auto_level_decref(void);
casadi_int joy_auto_level_n_in(void);
casadi_int joy_auto_level_n_out(void);
casadi_real joy_auto_level_default_in(casadi_int i);
const char* joy_auto_level_name_in(casadi_int i);
const char* joy_auto_level_name_out(casadi_int i);
const casadi_int* joy_auto_level_sparsity_in(casadi_int i);
const casadi_int* joy_auto_level_sparsity_out(casadi_int i);
int joy_auto_level_work(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w);
int joy_auto_level_work_bytes(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w);
#define joy_auto_level_SZ_ARG 7
#define joy_auto_level_SZ_RES 2
#define joy_auto_level_SZ_IW 0
#define joy_auto_level_SZ_W 28
int strapdown_ins_propagate(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem);
int strapdown_ins_propagate_alloc_mem(void);
int strapdown_ins_propagate_init_mem(int mem);
void strapdown_ins_propagate_free_mem(int mem);
int strapdown_ins_propagate_checkout(void);
void strapdown_ins_propagate_release(int mem);
void strapdown_ins_propagate_incref(void);
void strapdown_ins_propagate_decref(void);
casadi_int strapdown_ins_propagate_n_in(void);
casadi_int strapdown_ins_propagate_n_out(void);
casadi_real strapdown_ins_propagate_default_in(casadi_int i);
const char* strapdown_ins_propagate_name_in(casadi_int i);
const char* strapdown_ins_propagate_name_out(casadi_int i);
const casadi_int* strapdown_ins_propagate_sparsity_in(casadi_int i);
const casadi_int* strapdown_ins_propagate_sparsity_out(casadi_int i);
int strapdown_ins_propagate_work(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w);
int strapdown_ins_propagate_work_bytes(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w);
#define strapdown_ins_propagate_SZ_ARG 5
#define strapdown_ins_propagate_SZ_RES 1
#define strapdown_ins_propagate_SZ_IW 0
#define strapdown_ins_propagate_SZ_W 45
int control_allocation(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem);
int control_allocation_alloc_mem(void);
int control_allocation_init_mem(int mem);
void control_allocation_free_mem(int mem);
int control_allocation_checkout(void);
void control_allocation_release(int mem);
void control_allocation_incref(void);
void control_allocation_decref(void);
casadi_int control_allocation_n_in(void);
casadi_int control_allocation_n_out(void);
casadi_real control_allocation_default_in(casadi_int i);
const char* control_allocation_name_in(casadi_int i);
const char* control_allocation_name_out(casadi_int i);
const casadi_int* control_allocation_sparsity_in(casadi_int i);
const casadi_int* control_allocation_sparsity_out(casadi_int i);
int control_allocation_work(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w);
int control_allocation_work_bytes(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w);
#define control_allocation_SZ_ARG 6
#define control_allocation_SZ_RES 1
#define control_allocation_SZ_IW 0
#define control_allocation_SZ_W 25
#ifdef __cplusplus
} /* extern "C" */
#endif
