#include "tuple_parser.hpp"

#include <boost/python.hpp>

struct node_to_python_converter
{
  static PyObject *convert(const node::ptr &node)
  {
    if ( ! node ) {
      return boost::python::incref(boost::python::object().ptr());
    }
    boost::python::object result;
    if ( node->type == node::TEXT ) {
      auto ptr = std::dynamic_pointer_cast<text_node>(node);
      result = boost::python::object(ptr->text);
    } else if ( node->type == node::TUPLE ) {
      auto ptr = std::dynamic_pointer_cast<tuple_node>(node);
      result = boost::python::object(ptr->nodes);
    }
    return boost::python::incref(result.ptr());
  }
};

struct node_list_to_python_converter
{
  static PyObject *convert(const node_list &node)
  {
    boost::python::list list;
    for(auto child : node){
      list.append(child);
    }
    return boost::python::incref(
        boost::python::tuple(list).ptr());
  }
};

boost::python::object pyparse(const std::string &str)
{
  auto ret = parse(str);
  if ( ! ret ) {
    return boost::python::tuple();
  }
  return boost::python::object(ret);
}

BOOST_PYTHON_MODULE(tuple_parser)
{
  boost::python::def("parse", pyparse);

  // node::ptr
  boost::python::to_python_converter<node::ptr,
      node_to_python_converter>();

  // node_list
  boost::python::to_python_converter<node_list,
      node_list_to_python_converter>();
}
