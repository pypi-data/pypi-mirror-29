#ifndef TH_GENERIC_FILE
#define TH_GENERIC_FILE "generic/cpu.c"
#else

void cluster_(grid)(int C, THLongTensor *output, THTensor *position, THTensor *size, THLongTensor *count) {
  real *size_data = size->storage->data + size->storageOffset;
  int64_t *count_data = count->storage->data + count->storageOffset;
  int64_t D, d, i, c, tmp;
  D = THTensor_(nDimension)(position);
  d = THTensor_(size)(position, D - 1);
  TH_TENSOR_DIM_APPLY2(int64_t, output, real, position, D - 1,
    tmp = C; c = 0;
    for (i = 0; i < d; i++) {
      tmp = tmp / *(count_data + i);
      c += tmp * (int64_t) (*(position_data + i * position_stride) / *(size_data + i));
    }
    output_data[0] = c;
  )
}

#endif
